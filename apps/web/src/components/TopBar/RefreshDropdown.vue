<template>
  <n-popselect
    :value="currentRefreshIntervalStore.value"
    :options="intervals"
    scrollable
    style="width: 92px; height: 164px;"
    @update:value="onIntervalChange"
  >
    <n-button round class="refresh-button">
      {{ currentRefreshIntervalStore.label }}
    </n-button>
  </n-popselect>
</template>

<script>
import { NButton, NPopselect } from 'naive-ui';

import { useCurrentRefreshIntervalStore } from '@/stores/currentRefreshIntervalStore';
import { REFRESH_INTERVAL_OPTIONS } from '@/utils/intervals';

export default {
  name: 'RefreshDropdown',

  components: {
    NButton,
    NPopselect,
  },

  data() {
    return {
      currentRefreshIntervalStore: useCurrentRefreshIntervalStore(),
      intervals: REFRESH_INTERVAL_OPTIONS,
    };
  },

  methods: {
    onIntervalChange(value, option) {
      this.currentRefreshIntervalStore.setCurrentInterval(option ?? { value });
    },
  },
};
</script>

<style scoped>
.refresh-button {
  width: 92px;
}
</style>
