export const PROBE_OPTIONS = [
  { label: 'Gateway Health', value: 'health' },
];

export const PROBE_CONFIG = {
  health: {
    label: 'Gateway Health',
    path: '/health',
    accent: '#ff9466',
    description: 'Aggregated API gateway health across downstream services.',
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
