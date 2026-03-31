#!/bin/sh
set -eu

API_GATEWAY_PORT="${API_GATEWAY_PORT:-8080}"
FRONTEND_PORT="${FRONTEND_PORT:-5173}"

cat >/app/dist/runtime-config.js <<EOF
window.__TREND_BUDDY_CONFIG__ = Object.freeze({
  apiBaseUrl: window.location.protocol + '//' + (window.location.hostname || 'localhost') + ':${API_GATEWAY_PORT}'
});
EOF

exec serve -s /app/dist -l "${FRONTEND_PORT}"
