<template>
  <div id="chart-wrapper">
    <section class="chart-stage">
      <div class="chart-header">
        <div>
          <p class="eyebrow">Telemetry feed</p>
          <h2>{{ selectedProbe.label }} endpoint trace</h2>
          <p class="chart-copy">
            {{ selectedProbe.description }} The latency chart below keeps the root and health probes
            visible together so the backend drift is easy to spot.
          </p>
        </div>

        <div class="headline-metrics">
          <div class="headline-chip">
            <span>Last latency</span>
            <strong>{{ formatDuration(selectedRecord.latencyMs) }}</strong>
          </div>

          <div class="headline-chip">
            <span>Success rate</span>
            <strong>{{ successRate(selectedRecord) }}</strong>
          </div>

          <div class="headline-chip">
            <span>Last check</span>
            <strong>{{ formatRelativeTime(selectedRecord.lastCheckedAt) }}</strong>
          </div>
        </div>
      </div>

      <div ref="chartContainer" id="lightweight-chart" class="chart-container" />

      <div class="legend">
        <button
          v-for="probe in probeSeries"
          :key="probe.value"
          class="legend-pill"
          :class="{ active: currentEndpointStore.value === probe.value }"
          @click="currentEndpointStore.setEndpoint(probe.value)"
        >
          <span class="legend-swatch" :style="{ background: probe.accent, color: probe.accent }" />

          <span class="legend-copy">
            <span>{{ probe.label }}</span>
            <strong>{{ formatDuration(probe.latencyMs) }}</strong>
          </span>

          <n-tag size="small" round :type="toneForStatus(probe.status)">
            {{ labelForStatus(probe.status) }}
          </n-tag>
        </button>
      </div>
    </section>

    <aside class="signal-stack">
      <n-card class="signal-card" embedded>
        <template #header>
          Snapshot
        </template>

        <div class="snapshot-grid">
          <div class="snapshot-item">
            <span>Endpoint</span>
            <strong>{{ selectedProbe.path }}</strong>
          </div>

          <div class="snapshot-item">
            <span>Status</span>
            <strong>{{ labelForStatus(selectedRecord.status) }}</strong>
          </div>

          <div class="snapshot-item">
            <span>HTTP code</span>
            <strong>{{ selectedRecord.code ?? '--' }}</strong>
          </div>

          <div class="snapshot-item">
            <span>Checked at</span>
            <strong>{{ formatTimestamp(selectedRecord.lastCheckedAt) }}</strong>
          </div>
        </div>

        <div v-if="selectedRecord.error" class="error-banner">
          {{ selectedRecord.error }}
        </div>

        <pre class="payload-block">{{ selectedPayload }}</pre>
      </n-card>

      <n-card class="signal-card" embedded>
        <template #header>
          Payload metrics
        </template>

        <div v-if="selectedResponseEntries.length" class="metrics-grid">
          <div v-for="entry in selectedResponseEntries" :key="entry.key" class="metric-card">
            <span>{{ entry.label }}</span>
            <strong>{{ entry.value }}</strong>
          </div>
        </div>

        <p v-else class="empty-copy">
          No structured payload has been captured for the selected endpoint yet.
        </p>
      </n-card>

      <n-card class="signal-card" embedded>
        <template #header>
          Probe feed
        </template>

        <n-spin :show="probeTelemetryStore.isRefreshing">
          <ul class="feed-list">
            <li v-for="event in probeTelemetryStore.history" :key="event.id" class="feed-entry">
              <div class="feed-title-row">
                <strong>{{ event.label }}</strong>
                <n-tag size="small" round :type="toneForStatus(event.status)">
                  {{ labelForStatus(event.status) }}
                </n-tag>
              </div>

              <div class="feed-meta">
                <span>{{ event.url }}</span>
                <span>{{ formatTimestamp(event.checkedAt) }}</span>
              </div>

              <div class="feed-foot">
                <span>{{ formatDuration(event.latencyMs) }}</span>
                <span>HTTP {{ event.code ?? '--' }}</span>
              </div>

              <p class="feed-preview">
                {{ event.message || event.preview }}
              </p>
            </li>
          </ul>
        </n-spin>
      </n-card>
    </aside>
  </div>
</template>

<script>
import { NCard, NSpin, NTag } from 'naive-ui';

import { useCurrentEndpointStore } from '@/stores/currentEndpointStore';
import { useProbeTelemetryStore } from '@/stores/probeTelemetryStore';
import {
  formatDuration,
  formatJson,
  formatLabel,
  formatPercentage,
  formatRelativeTime,
  formatTimestamp,
} from '@/utils/formatting';
import { PROBE_CONFIG, PROBE_OPTIONS } from '@/utils/probes';
import { ChartManager } from '@/utils/chart';

export default {
  name: 'ChartArea',

  components: {
    NCard,
    NSpin,
    NTag,
  },

  data() {
    return {
      currentEndpointStore: useCurrentEndpointStore(),
      probeTelemetryStore: useProbeTelemetryStore(),
      chartManager: null,
    };
  },

  computed: {
    selectedProbe() {
      return PROBE_CONFIG[this.currentEndpointStore.value];
    },

    selectedRecord() {
      return this.probeTelemetryStore.records[this.currentEndpointStore.value];
    },

    selectedPayload() {
      if (this.selectedRecord.error) {
        return formatJson({
          error: this.selectedRecord.error,
        });
      }

      return formatJson(this.selectedRecord.responseBody);
    },

    selectedResponseEntries() {
      const payload = this.selectedRecord.responseBody;

      if (!payload || typeof payload !== 'object' || Array.isArray(payload)) {
        return [];
      }

      return Object.entries(payload).map(([key, value]) => ({
        key,
        label: formatLabel(key),
        value: typeof value === 'string' ? value : JSON.stringify(value),
      }));
    },

    probeSeries() {
      return PROBE_OPTIONS.map((option) => ({
        ...option,
        ...PROBE_CONFIG[option.value],
        ...this.probeTelemetryStore.records[option.value],
      }));
    },
  },

  watch: {
    'currentEndpointStore.value'() {
      this.syncChart();
    },

    'probeTelemetryStore.records': {
      deep: true,
      handler() {
        this.syncChart();
      },
    },
  },

  mounted() {
    this.initializeChart();
  },

  beforeUnmount() {
    this.destroyChart();
  },

  methods: {
    initializeChart() {
      this.chartManager = new ChartManager();
      this.chartManager.init(this.$refs.chartContainer);
      this.syncChart();
    },

    destroyChart() {
      if (this.chartManager) {
        this.chartManager.destroy();
        this.chartManager = null;
      }
    },

    syncChart() {
      if (!this.chartManager) {
        return;
      }

      this.chartManager.syncSeries(
        this.probeTelemetryStore.records,
        this.currentEndpointStore.value,
      );
    },

    formatDuration,
    formatRelativeTime,
    formatTimestamp,

    successRate(record) {
      return formatPercentage(record.successCount, record.totalChecks);
    },

    labelForStatus(status) {
      if (status === 'success') {
        return 'Live';
      }

      if (status === 'loading') {
        return 'Loading';
      }

      if (status === 'error') {
        return 'Error';
      }

      return 'Idle';
    },

    toneForStatus(status) {
      if (status === 'success') {
        return 'success';
      }

      if (status === 'loading') {
        return 'info';
      }

      if (status === 'error') {
        return 'error';
      }

      return 'default';
    },
  },
};
</script>

<style scoped>
#chart-wrapper {
  display: grid;
  grid-template-columns: minmax(0, 1.55fr) minmax(340px, 0.95fr);
  gap: 18px;
  align-items: start;
}

.chart-stage {
  padding: 22px;
  border-radius: 22px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background:
    linear-gradient(180deg, rgba(19, 23, 34, 0.94), rgba(7, 10, 16, 0.92)),
    rgba(7, 10, 16, 0.92);
  box-shadow: 0 28px 65px rgba(0, 0, 0, 0.35);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  align-items: start;
  margin-bottom: 18px;
}

.eyebrow {
  margin: 0 0 10px;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.48);
}

h2 {
  margin: 0;
  font-size: 28px;
  line-height: 1;
  letter-spacing: -0.04em;
}

.chart-copy {
  max-width: 680px;
  margin: 10px 0 0;
  color: rgba(255, 255, 255, 0.72);
  line-height: 1.65;
}

.headline-metrics {
  display: grid;
  gap: 10px;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  min-width: 340px;
}

.headline-chip {
  padding: 14px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.headline-chip span {
  display: block;
  margin-bottom: 8px;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: rgba(255, 255, 255, 0.48);
}

.headline-chip strong {
  display: block;
  font-size: 20px;
  color: rgba(255, 255, 255, 0.95);
}

.chart-container {
  height: 460px;
  border-radius: 18px;
  overflow: hidden;
  background:
    linear-gradient(180deg, rgba(87, 227, 176, 0.05), transparent 35%),
    linear-gradient(0deg, rgba(255, 148, 102, 0.05), transparent 28%),
    rgba(8, 12, 20, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.04);
}

.legend {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  margin-top: 14px;
}

.legend-pill {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 14px 16px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.025);
  color: inherit;
  text-align: left;
  cursor: pointer;
  transition: transform 180ms ease, border-color 180ms ease, background 180ms ease;
}

.legend-pill:hover,
.legend-pill.active {
  transform: translateY(-1px);
  border-color: rgba(255, 255, 255, 0.18);
  background: rgba(255, 255, 255, 0.05);
}

.legend-swatch {
  width: 10px;
  height: 38px;
  border-radius: 999px;
  box-shadow: 0 0 24px currentColor;
}

.legend-copy {
  display: grid;
  gap: 4px;
  flex: 1;
}

.legend-copy span {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.6);
}

.legend-copy strong {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.94);
}

.signal-stack {
  display: grid;
  gap: 18px;
}

.signal-card {
  border-radius: 22px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(10, 14, 21, 0.76);
  box-shadow: 0 20px 42px rgba(0, 0, 0, 0.22);
}

.snapshot-grid,
.metrics-grid {
  display: grid;
  gap: 10px;
}

.snapshot-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  margin-bottom: 14px;
}

.snapshot-item,
.metric-card {
  padding: 14px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.snapshot-item span,
.metric-card span {
  display: block;
  margin-bottom: 8px;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: rgba(255, 255, 255, 0.48);
}

.snapshot-item strong,
.metric-card strong {
  display: block;
  color: rgba(255, 255, 255, 0.92);
  line-height: 1.5;
  word-break: break-word;
}

.error-banner {
  margin-bottom: 14px;
  padding: 12px 14px;
  border-radius: 14px;
  border: 1px solid rgba(255, 115, 115, 0.28);
  background: rgba(255, 115, 115, 0.1);
  color: #ffd3d3;
}

.payload-block {
  max-height: 240px;
  margin: 0;
  padding: 14px;
  border-radius: 16px;
  overflow: auto;
  background: rgba(0, 0, 0, 0.24);
  border: 1px solid rgba(255, 255, 255, 0.06);
  color: rgba(255, 255, 255, 0.85);
  font-size: 12px;
  line-height: 1.65;
  white-space: pre-wrap;
  word-break: break-word;
}

.empty-copy {
  margin: 0;
  color: rgba(255, 255, 255, 0.58);
  line-height: 1.7;
}

.feed-list {
  display: grid;
  gap: 10px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.feed-entry {
  padding: 14px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.feed-title-row,
.feed-meta,
.feed-foot {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.feed-title-row {
  align-items: center;
  margin-bottom: 8px;
}

.feed-meta,
.feed-foot {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.56);
}

.feed-foot {
  margin-top: 8px;
}

.feed-preview {
  margin: 10px 0 0;
  color: rgba(255, 255, 255, 0.78);
  line-height: 1.6;
  word-break: break-word;
}

@media (max-width: 1180px) {
  #chart-wrapper {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 900px) {
  .chart-header {
    flex-direction: column;
  }

  .headline-metrics {
    width: 100%;
    min-width: 0;
    grid-template-columns: 1fr;
  }

  .legend {
    grid-template-columns: 1fr;
  }

  .snapshot-grid {
    grid-template-columns: 1fr;
  }
}
</style>
