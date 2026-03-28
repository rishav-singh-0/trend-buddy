<template>
  <div id="wrapper-select">
    <div class="brand-block">
      <div class="brand-row">
        <div>
          <p class="eyebrow">Trend Buddy</p>
          <h1>API Telemetry Terminal</h1>
        </div>

        <n-tag round size="medium" :type="systemTone">
          {{ systemLabel }}
        </n-tag>
      </div>

      <p class="brand-copy">
        Vue rebuild of the frontend, shaped around the algotrader layout: a top bar, a live
        telemetry chart, and a compact signal stack for backend responses.
      </p>
    </div>

    <div class="controls">
      <div class="endpoint-buttons">
        <n-button
          v-for="probe in probes"
          :key="probe.value"
          round
          strong
          :type="currentEndpointStore.value === probe.value ? 'primary' : 'default'"
          @click="currentEndpointStore.setEndpoint(probe.value)"
        >
          {{ probe.label }}
        </n-button>
      </div>

      <refresh-dropdown />

      <n-button round secondary strong :loading="probeTelemetryStore.isRefreshing" @click="probeTelemetryStore.probeAll()">
        Probe now
      </n-button>
    </div>

    <div class="telemetry-strip">
      <div class="telemetry-chip">
        <span>Base URL</span>
        <strong>{{ probeTelemetryStore.apiBaseUrl }}</strong>
      </div>

      <div class="telemetry-chip">
        <span>Auto-poll</span>
        <strong>{{ currentRefreshIntervalStore.label }}</strong>
      </div>

      <div class="telemetry-chip">
        <span>Last sync</span>
        <strong>{{ formatRelativeTime(probeTelemetryStore.lastCheckedAt) }}</strong>
      </div>
    </div>
  </div>
</template>

<script>
import { NButton, NTag } from 'naive-ui';

import RefreshDropdown from '@/components/TopBar/RefreshDropdown.vue';
import { useCurrentEndpointStore } from '@/stores/currentEndpointStore';
import { useCurrentRefreshIntervalStore } from '@/stores/currentRefreshIntervalStore';
import { useProbeTelemetryStore } from '@/stores/probeTelemetryStore';
import { formatRelativeTime } from '@/utils/formatting';
import { PROBE_OPTIONS } from '@/utils/probes';

export default {
  name: 'TheTopBar',

  components: {
    NButton,
    NTag,
    RefreshDropdown,
  },

  data() {
    return {
      currentEndpointStore: useCurrentEndpointStore(),
      currentRefreshIntervalStore: useCurrentRefreshIntervalStore(),
      probeTelemetryStore: useProbeTelemetryStore(),
      probes: PROBE_OPTIONS,
    };
  },

  computed: {
    systemLabel() {
      const records = this.probeTelemetryStore.records;
      const statuses = Object.values(records).map((record) => record.status);

      if (statuses.every((status) => status === 'idle')) {
        return 'Cold Start';
      }

      if (statuses.every((status) => status === 'success')) {
        return 'Live';
      }

      if (statuses.some((status) => status === 'loading')) {
        return 'Sweeping';
      }

      if (statuses.some((status) => status === 'success')) {
        return 'Partial';
      }

      return 'Degraded';
    },

    systemTone() {
      if (this.systemLabel === 'Live') {
        return 'success';
      }

      if (this.systemLabel === 'Sweeping') {
        return 'info';
      }

      if (this.systemLabel === 'Partial') {
        return 'warning';
      }

      if (this.systemLabel === 'Degraded') {
        return 'error';
      }

      return 'default';
    },
  },

  methods: {
    formatRelativeTime,
  },
};
</script>

<style scoped>
#wrapper-select {
  display: grid;
  gap: 18px;
  margin-bottom: 20px;
}

.brand-block {
  padding: 22px 24px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  background:
    linear-gradient(135deg, rgba(87, 227, 176, 0.12), transparent 45%),
    linear-gradient(225deg, rgba(255, 148, 102, 0.14), transparent 35%),
    rgba(17, 22, 34, 0.82);
  box-shadow: 0 24px 50px rgba(0, 0, 0, 0.28);
  backdrop-filter: blur(18px);
}

.brand-row {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: start;
}

.eyebrow {
  margin: 0 0 10px;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.56);
}

h1 {
  margin: 0;
  font-size: clamp(30px, 5vw, 46px);
  line-height: 0.95;
  letter-spacing: -0.04em;
}

.brand-copy {
  max-width: 820px;
  margin: 12px 0 0;
  color: rgba(255, 255, 255, 0.72);
  line-height: 1.65;
}

.controls {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}

.endpoint-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.telemetry-strip {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.telemetry-chip {
  padding: 14px 16px;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(10, 14, 21, 0.58);
}

.telemetry-chip span {
  display: block;
  margin-bottom: 6px;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: rgba(255, 255, 255, 0.48);
}

.telemetry-chip strong {
  display: block;
  font-size: 15px;
  line-height: 1.35;
  color: rgba(255, 255, 255, 0.92);
  word-break: break-word;
}

@media (max-width: 900px) {
  .brand-row {
    flex-direction: column;
  }

  .telemetry-strip {
    grid-template-columns: 1fr;
  }
}
</style>
