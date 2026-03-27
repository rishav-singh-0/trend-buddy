import { PRIVATE_API_BASE_URL } from '$env/static/private';
import { PUBLIC_API_BASE_URL } from '$env/static/public';
import type { PortfolioSummary } from '$lib/types';
import type { PageServerLoad } from './$types';

const fallbackPublicApiBaseUrl = 'http://localhost:3000';

export const load = (async ({ fetch }) => {
	const publicApiBaseUrl = PUBLIC_API_BASE_URL || fallbackPublicApiBaseUrl;
	const privateApiBaseUrl = PRIVATE_API_BASE_URL || publicApiBaseUrl;

	try {
		const response = await fetch(`${privateApiBaseUrl}/portfolio/summary`);
		if (!response.ok) {
			throw new Error(`Portfolio request failed with ${response.status}`);
		}

		const summary = (await response.json()) as PortfolioSummary;
		return {
			apiAvailable: true,
			apiBaseUrl: publicApiBaseUrl,
			summary
		};
	} catch (error) {
		console.warn('Trend Buddy API is unavailable for the dashboard spike.', error);
		return {
			apiAvailable: false,
			apiBaseUrl: publicApiBaseUrl,
			summary: null
		};
	}
}) satisfies PageServerLoad;
