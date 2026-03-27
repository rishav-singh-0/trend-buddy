import { PUBLIC_API_BASE_URL } from '$env/static/public';

const fallbackApiBaseUrl = 'http://localhost:3000';

export function getApiBaseUrl(): string {
	return PUBLIC_API_BASE_URL || fallbackApiBaseUrl;
}

export function getWebSocketBaseUrl(): string {
	return getApiBaseUrl().replace(/^http/, 'ws');
}
