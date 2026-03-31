import { defineStore } from 'pinia';

import { STORAGE_KEYS, getStoredState, setStoredState } from '@/utils/localStorage';
import { PROBE_OPTIONS } from '@/utils/probes';

function findProbe(value) {
  return PROBE_OPTIONS.find((option) => option.value === value) ?? PROBE_OPTIONS[0];
}

export const useCurrentEndpointStore = defineStore('currentEndpoint', {
  state: () => {
    const stored = getStoredState(STORAGE_KEYS.CURRENT_ENDPOINT);
    const currentProbe = findProbe(stored?.value);

    return {
      label: currentProbe.label,
      value: currentProbe.value,
    };
  },

  actions: {
    setEndpoint(value) {
      const nextProbe = findProbe(value);

      this.label = nextProbe.label;
      this.value = nextProbe.value;

      setStoredState(STORAGE_KEYS.CURRENT_ENDPOINT, {
        label: this.label,
        value: this.value,
      });
    },
  },
});
