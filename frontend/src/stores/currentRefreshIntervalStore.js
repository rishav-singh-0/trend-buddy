import { defineStore } from 'pinia';

import { normalizeRefreshInterval, REFRESH_INTERVAL_OPTIONS } from '@/utils/intervals';
import { STORAGE_KEYS, getStoredState, setStoredState } from '@/utils/localStorage';

function findInterval(value) {
  const normalizedValue = normalizeRefreshInterval(value);
  return REFRESH_INTERVAL_OPTIONS.find((option) => option.value === normalizedValue) ?? REFRESH_INTERVAL_OPTIONS[1];
}

export const useCurrentRefreshIntervalStore = defineStore('currentRefreshInterval', {
  state: () => {
    const stored = getStoredState(STORAGE_KEYS.CURRENT_REFRESH_INTERVAL);
    const currentInterval = findInterval(stored?.value);

    return {
      label: currentInterval.label,
      value: currentInterval.value,
    };
  },

  actions: {
    setCurrentInterval(option) {
      const nextInterval = findInterval(option?.value);

      this.label = nextInterval.label;
      this.value = nextInterval.value;

      setStoredState(STORAGE_KEYS.CURRENT_REFRESH_INTERVAL, {
        label: this.label,
        value: this.value,
      });
    },
  },
});
