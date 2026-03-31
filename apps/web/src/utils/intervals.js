export const REFRESH_INTERVAL_OPTIONS = [
  { label: '5s', value: 5000 },
  { label: '15s', value: 15000 },
  { label: '30s', value: 30000 },
  { label: '60s', value: 60000 },
];

const REFRESH_INTERVAL_VALUES = new Set(
  REFRESH_INTERVAL_OPTIONS.map((option) => option.value),
);

export function normalizeRefreshInterval(interval) {
  const numericInterval = Number(interval);

  if (REFRESH_INTERVAL_VALUES.has(numericInterval)) {
    return numericInterval;
  }

  return REFRESH_INTERVAL_OPTIONS[1].value;
}
