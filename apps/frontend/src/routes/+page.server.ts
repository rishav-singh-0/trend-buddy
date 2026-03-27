import { PRIVATE_API_BASE_URL } from '$env/static/private';
import { PUBLIC_API_BASE_URL } from '$env/static/public';
import type { ApiHealth, MarketSnapshot, PortfolioSummary } from '$lib/types';
import type { PageServerLoad } from './$types';

const fallbackPublicApiBaseUrl = 'http://localhost:3000';

export const load = (async ({ fetch }) => {
	const publicApiBaseUrl = PUBLIC_API_BASE_URL || fallbackPublicApiBaseUrl;
	const privateApiBaseUrl = PRIVATE_API_BASE_URL || publicApiBaseUrl;

	try {
		const [portfolioResponse, snapshotResponse, healthResponse] = await Promise.all([
			fetch(`${privateApiBaseUrl}/portfolio/summary`),
			fetch(`${privateApiBaseUrl}/market-data/snapshot`),
			fetch(`${privateApiBaseUrl}/health`)
		]);

		if (!portfolioResponse.ok) {
			throw new Error(`Portfolio request failed with ${portfolioResponse.status}`);
		}

		if (!snapshotResponse.ok) {
			throw new Error(`Market snapshot request failed with ${snapshotResponse.status}`);
		}

		if (!healthResponse.ok) {
			throw new Error(`Health request failed with ${healthResponse.status}`);
		}

		const [summary, snapshot, health] = (await Promise.all([
			portfolioResponse.json(),
			snapshotResponse.json(),
			healthResponse.json()
		])) as [PortfolioSummary, MarketSnapshot, ApiHealth];

		return {
			apiAvailable: true,
			apiBaseUrl: publicApiBaseUrl,
			health,
			snapshot,
			summary
		};
	} catch (error) {
		console.warn('Trend Buddy API is unavailable for the dashboard spike.', error);
		return {
			apiAvailable: false,
			apiBaseUrl: publicApiBaseUrl,
			health: null,
			snapshot: null,
			summary: null
		};
	}
}) satisfies PageServerLoad;
