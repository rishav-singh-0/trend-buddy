export const PROBE_OPTIONS = [
  { label: 'Root', value: 'root' },
  { label: 'Health', value: 'health' },
];

export const PROBE_CONFIG = {
  root: {
    label: 'Root',
    path: '/',
    accent: '#57e3b0',
    description: 'Base handshake for the Go API.',
  },
  health: {
    label: 'Health',
    path: '/health',
    accent: '#ff9466',
    description: 'Database health and pool telemetry.',
  },
};

export function normalizeBaseUrl(baseUrl) {
  const normalized = `${baseUrl ?? ''}`.trim();

  if (!normalized) {
    return '';
  }

  return normalized.endsWith('/') ? normalized.slice(0, -1) : normalized;
}

export function createProbeUrl(baseUrl, path) {
  const normalizedBaseUrl = normalizeBaseUrl(baseUrl);

  if (!normalizedBaseUrl) {
    return path === '/' ? '/' : path;
  }

  return path === '/' ? `${normalizedBaseUrl}/` : `${normalizedBaseUrl}${path}`;
}
