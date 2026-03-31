import { defineStore } from 'pinia';

import { PROBE_CONFIG, PROBE_OPTIONS, createProbeUrl, normalizeBaseUrl } from '@/utils/probes';

const DEFAULT_API_BASE_URL = 'http://localhost:8081';
const HISTORY_LIMIT = 16;
const SAMPLE_LIMIT = 48;

let pollTimer = null;
let historySequence = 0;

function createProbeRecord() {
  return {
    status: 'idle',
    code: null,
    latencyMs: null,
    lastCheckedAt: null,
    responseBody: null,
    error: null,
    totalChecks: 0,
    successCount: 0,
    samples: [],
  };
}

function createInitialRecords() {
  return PROBE_OPTIONS.reduce((records, option) => {
    records[option.value] = createProbeRecord();
    return records;
  }, {});
}

function parseResponseBody(rawBody) {
  if (!rawBody) {
    return null;
  }

  try {
    return JSON.parse(rawBody);
  } catch {
    return rawBody;
  }
}

function describeFailure(response, parsedBody) {
  if (typeof parsedBody === 'string' && parsedBody.trim()) {
    return parsedBody.trim();
  }

  if (parsedBody && typeof parsedBody === 'object' && parsedBody.message) {
    return parsedBody.message;
  }

  return response.statusText || 'Request failed';
}

function toPreview(payload) {
  if (payload === null || payload === undefined || payload === '') {
    return 'No payload';
  }

  const rawPreview =
    typeof payload === 'string'
      ? payload
      : JSON.stringify(payload);

  return rawPreview.length > 96 ? `${rawPreview.slice(0, 93)}...` : rawPreview;
}

function appendSample(samples, sample) {
  if (!sample) {
    return samples;
  }

  const nextSamples = [...samples];
  const lastSample = nextSamples[nextSamples.length - 1];

  if (lastSample && lastSample.time === sample.time) {
    nextSamples[nextSamples.length - 1] = sample;
  } else {
    nextSamples.push(sample);
  }

  return nextSamples.slice(-SAMPLE_LIMIT);
}

function buildHistoryEntry({ key, url, status, checkedAt, latencyMs, code, message, payload }) {
  historySequence += 1;

  return {
    id: `${key}-${historySequence}`,
    key,
    label: PROBE_CONFIG[key].label,
    url,
    status,
    checkedAt,
    latencyMs: Math.round(latencyMs),
    code,
    message,
    preview: toPreview(payload),
  };
}

function resolveApiBaseUrl() {
  return normalizeBaseUrl(import.meta.env.VITE_API_BASE_URL || DEFAULT_API_BASE_URL);
}

export const useProbeTelemetryStore = defineStore('probeTelemetry', {
  state: () => ({
    apiBaseUrl: resolveApiBaseUrl(),
    records: createInitialRecords(),
    history: [],
    pendingCount: 0,
    isBatchRefreshing: false,
  }),

  getters: {
    isRefreshing: (state) => state.pendingCount > 0 || state.isBatchRefreshing,
    lastCheckedAt: (state) =>
      Object.values(state.records).reduce(
        (latestTimestamp, record) => Math.max(latestTimestamp, record.lastCheckedAt ?? 0),
        0,
      ) || null,
  },

  actions: {
    async probe(key) {
      const config = PROBE_CONFIG[key];

      if (!config) {
        return null;
      }

      const url = createProbeUrl(this.apiBaseUrl, config.path);
      const currentRecord = this.records[key];
      const startedAt = Date.now();
      const startMark = performance.now();

      this.pendingCount += 1;
      this.records[key] = {
        ...currentRecord,
        status: 'loading',
        error: null,
      };

      try {
        const response = await fetch(url, {
          method: 'GET',
          headers: {
            Accept: 'application/json',
          },
        });

        const rawBody = await response.text();
        const parsedBody = parseResponseBody(rawBody);
        const latencyMs = performance.now() - startMark;
        const isSuccessful = response.ok;
        const nextRecord = {
          ...currentRecord,
          status: isSuccessful ? 'success' : 'error',
          code: response.status,
          latencyMs,
          lastCheckedAt: startedAt,
          responseBody: parsedBody,
          error: isSuccessful ? null : describeFailure(response, parsedBody),
          totalChecks: currentRecord.totalChecks + 1,
          successCount: isSuccessful ? currentRecord.successCount + 1 : currentRecord.successCount,
          samples: isSuccessful
            ? appendSample(currentRecord.samples, {
                time: Math.floor(startedAt / 1000),
                value: Number(latencyMs.toFixed(2)),
              })
            : currentRecord.samples,
        };

        this.records[key] = nextRecord;
        this.history = [
          buildHistoryEntry({
            key,
            url,
            status: nextRecord.status,
            checkedAt: startedAt,
            latencyMs,
            code: response.status,
            message: nextRecord.error,
            payload: parsedBody,
          }),
          ...this.history,
        ].slice(0, HISTORY_LIMIT);

        return parsedBody;
      } catch (error) {
        const latencyMs = performance.now() - startMark;
        const message = error instanceof Error ? error.message : 'Unexpected network error';
        const nextRecord = {
          ...currentRecord,
          status: 'error',
          code: null,
          latencyMs,
          lastCheckedAt: startedAt,
          responseBody: null,
          error: message,
          totalChecks: currentRecord.totalChecks + 1,
          successCount: currentRecord.successCount,
          samples: currentRecord.samples,
        };

        this.records[key] = nextRecord;
        this.history = [
          buildHistoryEntry({
            key,
            url,
            status: nextRecord.status,
            checkedAt: startedAt,
            latencyMs,
            code: null,
            message,
            payload: null,
          }),
          ...this.history,
        ].slice(0, HISTORY_LIMIT);

        return null;
      } finally {
        this.pendingCount = Math.max(0, this.pendingCount - 1);
      }
    },

    async probeAll() {
      if (this.isBatchRefreshing) {
        return;
      }

      this.isBatchRefreshing = true;

      try {
        await Promise.all(
          PROBE_OPTIONS.map((option) => this.probe(option.value)),
        );
      } finally {
        this.isBatchRefreshing = false;
      }
    },

    startPolling(intervalMs) {
      this.stopPolling();

      pollTimer = window.setInterval(() => {
        this.probeAll();
      }, intervalMs);
    },

    stopPolling() {
      if (pollTimer) {
        window.clearInterval(pollTimer);
        pollTimer = null;
      }
    },

    async bootstrap(intervalMs) {
      await this.probeAll();
      this.startPolling(intervalMs);
    },
  },
});
