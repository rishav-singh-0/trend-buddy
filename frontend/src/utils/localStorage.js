export const STORAGE_KEYS = {
  CURRENT_ENDPOINT: 'trendbuddy_current_endpoint',
  CURRENT_REFRESH_INTERVAL: 'trendbuddy_current_refresh_interval',
};

export function getStoredState(key, defaultValue = null) {
  try {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : defaultValue;
  } catch (error) {
    console.warn(`Failed to parse localStorage key "${key}":`, error);
    return defaultValue;
  }
}

export function setStoredState(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch (error) {
    console.error(`Failed to save to localStorage key "${key}":`, error);
  }
}
