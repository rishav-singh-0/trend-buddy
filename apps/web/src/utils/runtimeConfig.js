function resolveRuntimeConfig() {
  if (typeof window === 'undefined') {
    return {};
  }

  return window.__TREND_BUDDY_CONFIG__ ?? {};
}

export function resolveApiBaseUrl() {
  const runtimeConfig = resolveRuntimeConfig();
  const configuredBaseUrl = `${runtimeConfig.apiBaseUrl ?? import.meta.env.VITE_API_BASE_URL ?? ''}`.trim();

  if (configuredBaseUrl) {
    return configuredBaseUrl;
  }

  const { protocol, hostname } = window.location;
  const normalizedProtocol = protocol === 'https:' ? 'https:' : 'http:';
  const normalizedHostname = hostname || 'localhost';

  return `${normalizedProtocol}//${normalizedHostname}:8080`;
}
