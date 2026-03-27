<script lang="ts">
	import { browser } from '$app/environment';
	import LiveTicker from '$lib/components/LiveTicker.svelte';
	import { getWebSocketBaseUrl } from '$lib/api';
	import type { MarketSnapshot } from '$lib/types';
	import { onMount } from 'svelte';
	import type { PageData } from './$types';

	export let data: PageData;

	let liveTick: MarketSnapshot | null = null;
	let connectionState = 'connecting';

	const formatCurrency = (value: number) =>
		new Intl.NumberFormat('en-IN', {
			style: 'currency',
			currency: 'INR',
			maximumFractionDigits: 0
		}).format(value);

	function buildChartPath(values: number[]): string {
		if (!values.length) {
			return '';
		}

		const width = 520;
		const height = 180;
		const min = Math.min(...values);
		const max = Math.max(...values);
		const range = max - min || 1;

		return values
			.map((value, index) => {
				const x = (index / Math.max(values.length - 1, 1)) * width;
				const y = height - ((value - min) / range) * height;
				return `${index === 0 ? 'M' : 'L'} ${x.toFixed(2)} ${y.toFixed(2)}`;
			})
			.join(' ');
	}

	$: curve = data.summary?.equity_curve ?? [];
	$: chartPath = buildChartPath(curve.map((point) => point.close));

	onMount(() => {
		if (!browser) {
			return;
		}

		const socket = new WebSocket(`${getWebSocketBaseUrl()}/ws/market-data?symbol=NSE:NIFTY50`);
		connectionState = 'connecting';

		socket.addEventListener('open', () => {
			connectionState = 'connected';
		});

		socket.addEventListener('message', (event) => {
			liveTick = JSON.parse(event.data) as MarketSnapshot;
		});

		socket.addEventListener('close', () => {
			connectionState = 'disconnected';
		});

		socket.addEventListener('error', () => {
			connectionState = 'error';
		});

		return () => {
			socket.close();
		};
	});
</script>

<svelte:head>
	<title>Trend Buddy Dashboard Spike</title>
	<meta
		name="description"
		content="FastAPI plus SvelteKit spike for market snapshots, portfolio overview, and live websocket updates."
	/>
</svelte:head>

<div class="page-shell">
	<section class="hero">
		<div class="hero-copy">
			<p class="eyebrow">Trend Buddy</p>
			<h1>Fast, typed market workflows without a heavy shell.</h1>
			<p class="lede">
				This spike wires a FastAPI backend to a SvelteKit dashboard with domain routes, typed
				responses, and a live market pulse over WebSockets.
			</p>
		</div>

		<div class="hero-stats">
			<div class="panel">
				<p class="label">API status</p>
				<strong>{data.apiAvailable ? 'connected' : 'offline fallback'}</strong>
				<p class="muted">{data.apiBaseUrl}</p>
			</div>

			{#if data.summary}
				<div class="panel">
					<p class="label">Portfolio value</p>
					<strong>{formatCurrency(data.summary.total_value)}</strong>
					<p class="muted">Top sector: {data.summary.top_sector}</p>
				</div>
			{/if}
		</div>
	</section>

	<div class="dashboard-grid">
		<section class="panel chart-panel">
			<div class="section-head">
				<div>
					<p class="eyebrow">Portfolio</p>
					<h2>Equity curve</h2>
				</div>
				{#if data.summary}
					<p class={`pill ${data.summary.daily_pnl >= 0 ? 'gain' : 'loss'}`}>
						{formatCurrency(data.summary.daily_pnl)} today
					</p>
				{/if}
			</div>

			{#if data.summary}
				<div class="chart-frame">
					<svg viewBox="0 0 520 180" role="img" aria-label="Portfolio equity curve">
						<defs>
							<linearGradient id="curve" x1="0%" y1="0%" x2="100%" y2="0%">
								<stop offset="0%" stop-color="#f6d365" />
								<stop offset="100%" stop-color="#fda085" />
							</linearGradient>
						</defs>
						<path d={chartPath} fill="none" stroke="url(#curve)" stroke-width="5" stroke-linecap="round" />
					</svg>
				</div>
				<div class="chart-labels">
					{#each curve as point}
						<span>{point.session}</span>
					{/each}
				</div>
			{:else}
				<p class="empty-state">Start the FastAPI backend to populate this panel from `/portfolio/summary`.</p>
			{/if}
		</section>

		<LiveTicker tick={liveTick} {connectionState} />

		<section class="panel holdings-panel">
			<div class="section-head">
				<div>
					<p class="eyebrow">Exposure</p>
					<h2>Current holdings</h2>
				</div>
				{#if data.summary}
					<p class="muted">{formatCurrency(data.summary.cash_balance)} cash</p>
				{/if}
			</div>

			{#if data.summary}
				<div class="holdings-list">
					{#each data.summary.holdings as holding}
						<div class="holding-row">
							<div>
								<strong>{holding.symbol}</strong>
								<p>{holding.sector}</p>
							</div>
							<div class="holding-metrics">
								<strong>{holding.allocation_pct.toFixed(1)}%</strong>
								<p class:gain={holding.pnl_pct >= 0} class:loss={holding.pnl_pct < 0}>
									{holding.pnl_pct.toFixed(1)}% P&amp;L
								</p>
							</div>
						</div>
					{/each}
				</div>
			{:else}
				<p class="empty-state">The UI is wired; data appears once the API is reachable.</p>
			{/if}
		</section>
	</div>
</div>

<style>
	:global(body) {
		margin: 0;
		background:
			radial-gradient(circle at top left, rgba(246, 211, 101, 0.18), transparent 32%),
			radial-gradient(circle at bottom right, rgba(253, 160, 133, 0.2), transparent 30%),
			linear-gradient(180deg, #111111 0%, #181512 55%, #0b0b0b 100%);
		color: #f5f5f0;
		font-family:
			"Iowan Old Style", "Palatino Linotype", "Book Antiqua", Palatino, Georgia, serif;
	}

	.page-shell {
		max-width: 1200px;
		margin: 0 auto;
		padding: 3rem 1.2rem 4rem;
	}

	.hero,
	.dashboard-grid {
		display: grid;
		gap: 1.25rem;
	}

	.hero {
		grid-template-columns: 2fr 1fr;
		align-items: end;
		margin-bottom: 1.25rem;
	}

	.dashboard-grid {
		grid-template-columns: minmax(0, 2fr) minmax(320px, 1fr);
	}

	.hero-copy h1,
	h2 {
		margin: 0;
	}

	.hero-copy h1 {
		font-size: clamp(2.6rem, 5vw, 4.8rem);
		line-height: 0.95;
		letter-spacing: -0.06em;
		max-width: 10ch;
	}

	.lede,
	.muted,
	.empty-state,
	.holding-row p,
	.chart-labels span {
		color: rgba(245, 245, 240, 0.72);
	}

	.lede {
		max-width: 60ch;
		margin-top: 1rem;
		font-size: 1.04rem;
	}

	.eyebrow,
	.label {
		text-transform: uppercase;
		letter-spacing: 0.16em;
		font-size: 0.72rem;
		color: #f6d365;
		margin: 0 0 0.5rem;
	}

	.panel {
		background: rgba(255, 255, 255, 0.04);
		border: 1px solid rgba(255, 255, 255, 0.08);
		border-radius: 24px;
		padding: 1.25rem;
		backdrop-filter: blur(18px);
		box-shadow: 0 18px 50px rgba(0, 0, 0, 0.22);
	}

	.hero-stats {
		display: grid;
		gap: 1rem;
	}

	.hero-stats strong,
	.holding-row strong {
		font-size: 1.4rem;
	}

	.chart-panel,
	.holdings-panel {
		display: grid;
		gap: 1.2rem;
	}

	.chart-panel {
		grid-column: 1 / 2;
	}

	.section-head {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1rem;
	}

	.chart-frame {
		padding: 1rem 0.5rem 0.25rem;
		background: linear-gradient(180deg, rgba(255, 255, 255, 0.04), rgba(255, 255, 255, 0.01));
		border-radius: 20px;
	}

	svg {
		width: 100%;
		height: auto;
	}

	.chart-labels {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(72px, 1fr));
		gap: 0.5rem;
		font-size: 0.72rem;
	}

	.holdings-list {
		display: grid;
		gap: 0.8rem;
	}

	.holding-row {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1rem;
		padding: 0.9rem 0;
		border-bottom: 1px solid rgba(255, 255, 255, 0.08);
	}

	.holding-row:last-child {
		border-bottom: none;
		padding-bottom: 0;
	}

	.holding-row p,
	.holding-row strong,
	.muted,
	.empty-state {
		margin: 0;
	}

	.holding-metrics {
		text-align: right;
	}

	.pill {
		border-radius: 999px;
		padding: 0.35rem 0.8rem;
		font-size: 0.82rem;
	}

	.gain {
		color: #86efac;
	}

	.loss {
		color: #fca5a5;
	}

	.pill.gain {
		background: rgba(134, 239, 172, 0.12);
	}

	.pill.loss {
		background: rgba(252, 165, 165, 0.12);
	}

	@media (max-width: 900px) {
		.hero,
		.dashboard-grid {
			grid-template-columns: 1fr;
		}

		.hero-copy h1 {
			max-width: none;
		}
	}
</style>
