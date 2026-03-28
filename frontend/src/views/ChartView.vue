<template>
  <div>
    <the-top-bar />
    <chart-area id="chart-area" />
  </div>
</template>

<script>
import ChartArea from '@/components/Chart/ChartArea.vue';
import TheTopBar from '@/components/TopBar/TheTopBar.vue';
import { useCurrentRefreshIntervalStore } from '@/stores/currentRefreshIntervalStore';
import { useProbeTelemetryStore } from '@/stores/probeTelemetryStore';

export default {
  name: 'ChartView',

  components: {
    ChartArea,
    TheTopBar,
  },

  data() {
    return {
      currentRefreshIntervalStore: useCurrentRefreshIntervalStore(),
      probeTelemetryStore: useProbeTelemetryStore(),
    };
  },

  watch: {
    'currentRefreshIntervalStore.value'(newValue, oldValue) {
      if (newValue !== oldValue) {
        this.probeTelemetryStore.startPolling(newValue);
      }
    },
  },

  async created() {
    await this.probeTelemetryStore.bootstrap(this.currentRefreshIntervalStore.value);
  },

  beforeUnmount() {
    this.probeTelemetryStore.stopPolling();
  },
};
</script>
