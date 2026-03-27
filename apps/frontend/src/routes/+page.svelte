<script lang="ts">
	import { browser } from '$app/environment';
	import { getWebSocketBaseUrl } from '$lib/api';
	import SymbolChart from '$lib/components/SymbolChart.svelte';
	import type { MarketSnapshot, PortfolioHolding, PortfolioSummary } from '$lib/types';
	import { onDestroy } from 'svelte';
	import type { PageData } from './$types';

	export let data: PageData;

	let liveTick: MarketSnapshot | null = null;
	let connectionState = 'connecting';
	let selectedSymbol = '';
	let currentInterval = '1D';
	let chartStage: HTMLElement | null = null;
	let socket: WebSocket | null = null;
	let activeSocketSymbol = '';

	const topNav = ['Dashboard', 'Market Data', 'Portfolio', 'Strategies', 'Backtests', 'Analysis'];
	const pageTabs = ['1', '2', '3', '4'];
	const chartIntervals = ['1D', '1W', '1M'];

	const formatCurrency = (value: number, maximumFractionDigits = 2) =>
		new Intl.NumberFormat('en-IN', {
			style: 'currency',
			currency: 'INR',
			maximumFractionDigits
		}).format(value);

	const formatCompactNumber = (value: number) =>
		new Intl.NumberFormat('en-IN', {
			maximumFractionDigits: 2,
			notation: 'compact'
		}).format(value);

	const formatSignedNumber = (value: number, fractionDigits = 2) =>
		`${value >= 0 ? '+' : ''}${value.toFixed(fractionDigits)}`;

	const formatPercent = (value: number) => `${formatSignedNumber(value)}%`;

	const formatTime = (value: string | null | undefined) =>
		value
			? new Date(value).toLocaleTimeString('en-IN', {
					hour: '2-digit',
					minute: '2-digit',
					second: '2-digit'
				})
			: '--';

	function getOpeningBalance(summary: PortfolioSummary | null): number {
		if (!summary) {
			return 0;
		}

		return summary.total_value - summary.daily_pnl;
	}

	function buildChartPath(values: number[], width: number, height: number, inset = 0): string {
		if (!values.length) {
			return '';
		}

		const min = Math.min(...values);
		const max = Math.max(...values);
		const range = max - min || 1;

		return values
			.map((value, index) => {
				const x = (index / Math.max(values.length - 1, 1)) * width;
				const y = height - ((value - min) / range) * (height - inset) - inset / 2;
				return `${index === 0 ? 'M' : 'L'} ${x.toFixed(2)} ${y.toFixed(2)}`;
			})
			.join(' ');
	}

	function segmentStyle(index: number): string {
		const palette = ['#5372e7', '#5d7cef', '#53a4e4', '#4b8fdc', '#9135ab', '#6b46c1'];
		return palette[index % palette.length];
	}

	function getHoldingValue(holding: PortfolioHolding, totalValue: number): number {
		return (holding.allocation_pct / 100) * totalValue;
	}

	$: summary = data.summary;
	$: health = data.health;
	$: initialSnapshot = data.snapshot;
	$: holdings = summary?.holdings ?? [];
	$: curve = summary?.equity_curve ?? [];
	$: sortedHoldings = [...holdings].sort((left, right) => right.allocation_pct - left.allocation_pct);
	$: watchlist = sortedHoldings.slice(0, 4);
	$: if (!selectedSymbol) {
		selectedSymbol = watchlist[0]?.symbol ?? initialSnapshot?.symbol ?? 'NSE:NIFTY50';
	}
	$: selectedHolding = sortedHoldings.find((holding) => holding.symbol === selectedSymbol) ?? null;
	$: serverSnapshot = initialSnapshot?.symbol === selectedSymbol ? initialSnapshot : null;
	$: activeSnapshot = liveTick ?? serverSnapshot;
	$: openingBalance = getOpeningBalance(summary);
	$: usedCapital = summary ? Math.max(summary.total_value - summary.cash_balance, 0) : 0;
	$: holdingsCurrentValue = summary?.total_value ?? 0;
	$: holdingsInvestment = summary ? Math.max(summary.total_value - summary.total_pnl, 0) : 0;
	$: holdingsPnlPct =
		holdingsInvestment > 0 ? ((holdingsCurrentValue - holdingsInvestment) / holdingsInvestment) * 100 : 0;
	$: totalAllocation = sortedHoldings.reduce((sum, holding) => sum + holding.allocation_pct, 0);
	$: holdingsChartPath = buildChartPath(curve.map((point) => point.close), 460, 136, 18);
	$: topHolding = sortedHoldings[0] ?? null;
	$: firstSession = curve[0]?.session ?? '--';
	$: middleSession = curve[Math.floor(curve.length / 2)]?.session ?? '--';
	$: lastSession = curve[curve.length - 1]?.session ?? '--';
	$: selectedSymbolPrice = activeSnapshot?.price ?? (selectedHolding ? getHoldingValue(selectedHolding, holdingsCurrentValue) : null);

	function connectMarketStream(symbol: string) {
		if (!browser || !symbol || activeSocketSymbol === symbol) {
			return;
		}

		activeSocketSymbol = symbol;
		liveTick = null;
		socket?.close();

		const nextSocket = new WebSocket(`${getWebSocketBaseUrl()}/ws/market-data?symbol=${encodeURIComponent(symbol)}`);
		socket = nextSocket;
		connectionState = 'connecting';

		nextSocket.addEventListener('open', () => {
			if (socket !== nextSocket) {
				return;
			}
			connectionState = 'connected';
		});

		nextSocket.addEventListener('message', (event) => {
			if (socket !== nextSocket) {
				return;
			}
			liveTick = JSON.parse(event.data) as MarketSnapshot;
		});

		nextSocket.addEventListener('close', () => {
			if (socket !== nextSocket) {
				return;
			}
			connectionState = 'disconnected';
		});

		nextSocket.addEventListener('error', () => {
			if (socket !== nextSocket) {
				return;
			}
			connectionState = 'error';
		});
	}

	function openChartForSymbol(symbol: string) {
		selectedSymbol = symbol;
		chartStage?.scrollIntoView({ behavior: 'smooth', block: 'start' });
	}

	onDestroy(() => {
		socket?.close();
	});

	$: if (browser && selectedSymbol) {
		connectMarketStream(selectedSymbol);
	}
</script>

<svelte:head>
	<title>Trend Buddy Dashboard</title>
	<meta
		name="description"
		content="Dark trading dashboard for Trend Buddy portfolio, market data, strategies, backtests, and analysis."
	/>
</svelte:head>

<div class="terminal">
	<header class="topbar">
		<div class="ticker-strip">
			<div class="index-chip">
				<span class="index-name">{activeSnapshot?.symbol ?? 'NSE:NIFTY50'}</span>
				<strong>{activeSnapshot ? activeSnapshot.price.toFixed(2) : '--'}</strong>
				<span class:down={(activeSnapshot?.change_pct ?? 0) < 0} class:up={(activeSnapshot?.change_pct ?? 0) >= 0}>
					{activeSnapshot ? formatPercent(activeSnapshot.change_pct) : '--'}
				</span>
			</div>
			<div class="index-chip">
				<span class="index-name">Portfolio</span>
				<strong>{summary ? formatCompactNumber(summary.total_value) : '--'}</strong>
				<span class:down={(summary?.daily_pnl ?? 0) < 0} class:up={(summary?.daily_pnl ?? 0) >= 0}>
					{summary ? formatCurrency(summary.daily_pnl, 0) : '--'}
				</span>
			</div>
		</div>

		<div class="workspace-switcher">
			<button type="button" aria-label="Previous workspace">&lt;</button>
			<div class="workspace-pill">
				<span>Trend Buddy</span>
				<em>{data.apiAvailable ? 'LIVE' : 'OFFLINE'}</em>
			</div>
			<button type="button" aria-label="App grid">[]</button>
		</div>

		<nav class="main-nav" aria-label="Main navigation">
			{#each topNav as item, index}
				<button class:active={index === 0} type="button">{item}</button>
			{/each}
		</nav>

		<div class="profile-actions">
			<span class="icon"></span>
			<span class="icon"></span>
			<div class="user-badge">
				<span class:live-dot={data.apiAvailable} class="user-dot"></span>
				<strong>{health?.status ?? 'unavailable'}</strong>
			</div>
		</div>
	</header>

	<div class="content-shell">
		<aside class="marketwatch">
			<div class="search-box">
				<span class="search-icon"></span>
				<input type="text" placeholder="Search symbols, holdings, strategies, backtests" />
				<kbd>Ctrl + K</kbd>
			</div>

			<div class="watchlist-meta">
				<span>Holdings watchlist ({watchlist.length} / {holdings.length || 0})</span>
				<button type="button">Top allocations</button>
			</div>

			<section class="watchlist-card">
				<div class="watchlist-header">Portfolio holdings</div>

				{#if watchlist.length}
					{#each watchlist as holding}
						<div
							class:selected-row={selectedSymbol === holding.symbol}
							class="watchlist-row"
							on:click={() => openChartForSymbol(holding.symbol)}
							on:keydown={(event) => {
								if (event.key === 'Enter' || event.key === ' ') {
									event.preventDefault();
									openChartForSymbol(holding.symbol);
								}
							}}
							role="button"
							tabindex="0"
						>
							<div class="watchlist-main">
								<div class="watchlist-labels">
									<strong>{holding.symbol}</strong>
									<span>{holding.sector}</span>
								</div>
								<div class="watchlist-stats">
									<span>{formatCurrency(getHoldingValue(holding, holdingsCurrentValue), 0)}</span>
									<span class:down={holding.pnl_pct < 0} class:up={holding.pnl_pct >= 0}>{formatPercent(holding.pnl_pct)}</span>
									<span class="watch-price">{holding.allocation_pct.toFixed(1)}%</span>
								</div>
							</div>
							<div class="watchlist-actions">
								<button class="buy-btn" type="button">B</button>
								<button class="sell-btn" type="button">S</button>
								<button class="chart-btn" type="button" on:click|stopPropagation={() => openChartForSymbol(holding.symbol)}>
									Chart
								</button>
							</div>
						</div>
					{/each}
				{:else}
					<div class="watchlist-empty">No holdings available. Start the API to populate the portfolio view.</div>
				{/if}
			</section>

			<div class="watchlist-footer">
				<div class="page-indicators">
					{#each pageTabs as tab, index}
						<button class:active={index === 0} type="button">{tab}</button>
					{/each}
				</div>
				<div class="footer-icons">
					<span></span>
					<span></span>
				</div>
			</div>
		</aside>

		<main class="dashboard">
			<section class="dashboard-head">
				<h1>Trend Buddy</h1>
				<p>Market data, portfolio tracking, backtest context, and strategy-facing analysis in one workspace.</p>
			</section>

			<section bind:this={chartStage} class="chart-stage section">
				<div class="chart-view-tabs">
					<button class="active" type="button">Chart</button>
					<button type="button">Overview</button>
				</div>

				<div class="chart-workspace">
					<div class="chart-panel">
						<div class="chart-toolbar">
							<div class="toolbar-left">
								<div class="selected-symbol">
									<h2>{selectedSymbol}</h2>
									<span>{selectedHolding?.sector ?? activeSnapshot?.signal ?? 'Market data view'}</span>
								</div>
								<div class="interval-tabs">
									{#each chartIntervals as interval}
										<button
											class:active={currentInterval === interval}
											type="button"
											on:click={() => {
												currentInterval = interval;
											}}
										>
											{interval}
										</button>
									{/each}
								</div>
							</div>

							<div class="toolbar-right">
								<button type="button">Indicators</button>
								<button type="button">Compare</button>
								<button type="button">Reset</button>
							</div>
						</div>

						<div class="chart-stats">
							<div class="stat-pill buy">
								<span>{selectedSymbolPrice ? selectedSymbolPrice.toFixed(2) : '--'}</span>
								<strong>BUY</strong>
							</div>
							<div class="stat-pill sell">
								<span>{selectedSymbolPrice ? selectedSymbolPrice.toFixed(2) : '--'}</span>
								<strong>SELL</strong>
							</div>
							<div class="chart-meta">
								<p><span>Signal</span><strong>{activeSnapshot?.signal ?? '--'}</strong></p>
								<p><span>WebSocket</span><strong>{connectionState}</strong></p>
								<p><span>Updated</span><strong>{formatTime(activeSnapshot?.generated_at)}</strong></p>
							</div>
						</div>

						<SymbolChart symbol={selectedSymbol} activePrice={selectedSymbolPrice} interval={currentInterval} />
					</div>

					<aside class="chart-sidebar">
						<div class="margin-card">
							<div class="margin-title">
								<span class="dot-icon"></span>
								<h2>Selected symbol</h2>
							</div>
							<div class="margin-body">
								<div class="primary-metric">
									<strong>{selectedSymbolPrice ? formatCompactNumber(selectedSymbolPrice) : '--'}</strong>
									<span>{selectedSymbol}</span>
								</div>
								<div class="vertical-rule"></div>
								<div class="secondary-metrics">
									<p><span>Change</span><strong>{activeSnapshot ? formatPercent(activeSnapshot.change_pct) : '--'}</strong></p>
									<p><span>Sector</span><strong>{selectedHolding?.sector ?? '--'}</strong></p>
									<p><span>Allocation</span><strong>{selectedHolding ? `${selectedHolding.allocation_pct.toFixed(1)}%` : '--'}</strong></p>
									<button class="statement-link" type="button">Endpoint: /market-data/candles</button>
								</div>
							</div>
						</div>

						<div class="margin-card">
							<div class="margin-title">
								<span class="dot-icon hollow"></span>
								<h2>Portfolio</h2>
							</div>
							<div class="margin-body">
								<div class="primary-metric">
									<strong>{summary ? formatCompactNumber(summary.total_value) : '--'}</strong>
									<span>Tracked book value</span>
								</div>
								<div class="vertical-rule"></div>
								<div class="secondary-metrics">
									<p><span>Cash balance</span><strong>{summary ? formatCompactNumber(summary.cash_balance) : '--'}</strong></p>
									<p><span>Capital used</span><strong>{summary ? formatCompactNumber(usedCapital) : '--'}</strong></p>
									<p><span>Top sector</span><strong>{summary?.top_sector ?? '--'}</strong></p>
									<button class="statement-link" type="button">Endpoint: /portfolio/summary</button>
								</div>
							</div>
						</div>

						<div class="margin-card compact">
							<div class="margin-title">
								<span class="dot-icon hollow"></span>
								<h2>API health</h2>
							</div>
							<div class="health-state">
								<span class:status-live={data.apiAvailable} class="status-badge">{health?.status ?? 'offline'}</span>
								<p>{data.apiBaseUrl}</p>
							</div>
						</div>
					</aside>
				</div>
			</section>

			<section class="holdings-section section">
				<div class="section-title">
					<h2>Holdings ({holdings.length})</h2>
				</div>

				<div class="holdings-summary">
					<div class="holdings-pnl">
						<strong class:positive={(summary?.total_pnl ?? 0) >= 0} class:negative={(summary?.total_pnl ?? 0) < 0}>
							{summary ? formatCompactNumber(summary.total_pnl) : '--'}
						</strong>
						<span class:positive={holdingsPnlPct >= 0} class:negative={holdingsPnlPct < 0}>
							{summary ? formatPercent(holdingsPnlPct) : '--'}
						</span>
						<p>Total P&amp;L</p>
					</div>

					<div class="vertical-rule"></div>

					<div class="holdings-metrics">
						<p><span>Current value</span><strong>{summary ? formatCompactNumber(holdingsCurrentValue) : '--'}</strong></p>
						<p><span>Investment</span><strong>{summary ? formatCompactNumber(holdingsInvestment) : '--'}</strong></p>
						<p><span>Opening balance</span><strong>{summary ? formatCompactNumber(openingBalance) : '--'}</strong></p>
					</div>
				</div>

				<div class="allocation-track" aria-label="Holdings allocation track">
					{#if sortedHoldings.length}
						{#each sortedHoldings.slice(0, 6) as holding, index}
							<span
								style={`width:${totalAllocation ? ((holding.allocation_pct / totalAllocation) * 100).toFixed(2) : (100 / Math.max(sortedHoldings.slice(0, 6).length, 1)).toFixed(2)}%; background:${segmentStyle(index)};`}
							></span>
						{/each}
					{:else}
						<span class="empty-allocation"></span>
					{/if}
				</div>

				<div class="allocation-footer">
					<strong>{summary ? formatCurrency(holdingsCurrentValue) : 'Portfolio unavailable'}</strong>
					<div class="legend">
						<span class="legend-item active"><i></i>Current value</span>
						<span class="legend-item"><i></i>Allocation</span>
						<span class="legend-item"><i></i>P&amp;L</span>
					</div>
				</div>
			</section>

			<section class="lower-grid section">
				<div class="overview-panel">
					<div class="section-title with-icon">
						<span class="panel-mark"></span>
						<h2>Backtest input curve</h2>
					</div>

					<div class="chart-legend">Portfolio equity curve</div>

					<div class="overview-chart">
						<svg viewBox="0 0 460 136" role="img" aria-label="Portfolio equity curve">
							<path class="grid-line" d="M 0 26 L 460 26" />
							<path class="grid-line" d="M 0 68 L 460 68" />
							<path class="grid-line" d="M 0 110 L 460 110" />
							<path
								class="market-line"
								d={holdingsChartPath || 'M 0 92 L 22 122 L 44 76 L 66 72 L 88 64 L 110 59 L 132 44 L 154 56 L 176 74 L 198 61 L 220 69 L 242 38 L 264 35 L 286 30 L 308 28 L 330 34 L 352 57 L 374 50 L 396 26 L 418 94 L 440 112 L 460 101'}
							/>
						</svg>
						<div class="chart-axis">
							<span>{firstSession}</span>
							<span>{middleSession}</span>
							<span>{lastSession}</span>
						</div>
					</div>
				</div>

				<div class="positions-panel">
					<div class="section-title">
						<h2>Analysis</h2>
					</div>

					<div class="analysis-list">
						<div class="analysis-item">
							<span class="position-marker"></span>
							<div>
								<strong>Signal</strong>
								<p>{activeSnapshot?.signal ?? 'Unavailable'}</p>
							</div>
						</div>

						<div class="analysis-item">
							<span class="position-marker"></span>
							<div>
								<strong>Top sector</strong>
								<p>{summary?.top_sector ?? 'Unavailable'}</p>
							</div>
						</div>

						<div class="analysis-item">
							<span class="position-marker"></span>
							<div>
								<strong>Largest holding</strong>
								<p>{topHolding ? `${topHolding.symbol} (${topHolding.allocation_pct.toFixed(1)}%)` : 'Unavailable'}</p>
							</div>
						</div>

						<div class="analysis-item">
							<span class="position-marker"></span>
							<div>
								<strong>Backtest history</strong>
								<p>{curve.length} equity sessions loaded</p>
							</div>
						</div>
					</div>

					<div class="stream-chip">
						<span class:status-live={connectionState === 'connected'}>{connectionState}</span>
						<strong>{health?.status ?? 'offline'}</strong>
					</div>
				</div>
			</section>
		</main>
	</div>
</div>

<style>
	:global(body) {
		margin: 0;
		background: #0f0f10;
		color: #e5e7eb;
		font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
	}

	:global(*) {
		box-sizing: border-box;
	}

	:global(button),
	:global(input) {
		font: inherit;
	}

	.terminal {
		min-height: 100vh;
		background: #141415;
	}

	.topbar {
		height: 39px;
		display: grid;
		grid-template-columns: 1.1fr auto 1.4fr auto;
		align-items: stretch;
		background: #1a1a1b;
		border-bottom: 1px solid #262628;
	}

	.ticker-strip,
	.workspace-switcher,
	.main-nav,
	.profile-actions {
		display: flex;
		align-items: center;
	}

	.ticker-strip,
	.workspace-switcher,
	.profile-actions {
		padding: 0 14px;
		gap: 16px;
		border-right: 1px solid #262628;
	}

	.index-chip {
		display: flex;
		align-items: center;
		gap: 6px;
		font-size: 12px;
		color: #8b8c90;
		white-space: nowrap;
	}

	.index-chip strong,
	.index-name {
		font-size: 12px;
	}

	.index-chip strong {
		color: #d96b56;
		font-weight: 600;
	}

	.up {
		color: #7cd992;
	}

	.down {
		color: #a96d61;
	}

	.workspace-switcher button,
	.main-nav button,
	.page-indicators button,
	.watchlist-meta button {
		border: none;
		background: transparent;
		color: inherit;
		cursor: pointer;
	}

	.workspace-switcher button {
		color: #d86a47;
		font-size: 13px;
		padding: 0;
	}

	.workspace-pill {
		min-width: 140px;
		height: 26px;
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 0 10px;
		background: #232325;
		border: 1px solid #2b2b2e;
		border-radius: 3px;
		color: #ceced2;
		font-size: 12px;
	}

	.workspace-pill em {
		font-style: normal;
		font-size: 10px;
		font-weight: 600;
		color: #e08c4d;
	}

	.main-nav {
		justify-content: center;
		gap: 2px;
	}

	.main-nav button {
		height: 100%;
		padding: 0 18px;
		font-size: 13px;
		color: #a3a3a8;
	}

	.main-nav button.active {
		color: #d26d4d;
	}

	.profile-actions {
		border-right: none;
		gap: 14px;
	}

	.icon,
	.search-icon,
	.footer-icons span,
	.dot-icon,
	.panel-mark {
		display: inline-block;
	}

	.icon {
		width: 11px;
		height: 11px;
		border: 1px solid #66686d;
		border-radius: 2px;
		opacity: 0.75;
	}

	.user-badge {
		display: flex;
		align-items: center;
		gap: 8px;
		font-size: 13px;
		color: #c3c3c7;
		text-transform: capitalize;
	}

	.user-dot {
		width: 16px;
		height: 16px;
		border-radius: 50%;
		background: #4a4a50;
	}

	.live-dot {
		background: #2f7a56;
		box-shadow: 0 0 0 3px rgba(57, 153, 99, 0.14);
	}

	.content-shell {
		display: grid;
		grid-template-columns: 414px minmax(0, 1fr);
		min-height: calc(100vh - 39px);
	}

	.marketwatch {
		display: grid;
		grid-template-rows: auto auto auto 1fr auto;
		padding: 12px;
		background: #171718;
		border-right: 1px solid #242426;
	}

	.search-box {
		height: 40px;
		display: grid;
		grid-template-columns: 18px minmax(0, 1fr) auto;
		align-items: center;
		gap: 10px;
		padding: 0 10px;
		border: 1px solid #28282b;
		border-radius: 3px;
		background: #151516;
		color: #6e6f74;
	}

	.search-icon {
		width: 10px;
		height: 10px;
		border: 1px solid #64666b;
		border-radius: 50%;
		position: relative;
	}

	.search-icon::after {
		content: '';
		position: absolute;
		right: -4px;
		bottom: -3px;
		width: 5px;
		height: 1px;
		background: #64666b;
		transform: rotate(45deg);
	}

	.search-box input {
		border: none;
		outline: none;
		background: transparent;
		color: #9e9fa4;
		font-size: 13px;
	}

	.search-box kbd {
		padding: 3px 8px;
		border: 1px solid #333338;
		border-radius: 3px;
		background: #1b1b1c;
		color: #8a8b90;
		font-size: 12px;
	}

	.watchlist-meta,
	.watchlist-footer,
	.watchlist-row,
	.watchlist-main,
	.watchlist-stats,
	.allocation-footer,
	.legend,
	.holdings-summary,
	.margin-title,
	.margin-body,
	.secondary-metrics p,
	.holdings-metrics p,
	.section-title,
	.stream-chip,
	.analysis-item,
	.watchlist-labels {
		display: flex;
		align-items: center;
	}

	.watchlist-meta,
	.watchlist-footer,
	.allocation-footer,
	.holdings-summary,
	.margin-body,
	.section-title,
	.stream-chip,
	.watchlist-row,
	.secondary-metrics p,
	.holdings-metrics p {
		justify-content: space-between;
	}

	.watchlist-meta {
		margin: 14px 4px 10px;
		font-size: 12px;
		color: #7b7c82;
	}

	.watchlist-meta button {
		color: #5a84ff;
		font-size: 12px;
	}

	.watchlist-card {
		border: 1px solid #262629;
		border-radius: 2px;
		background: #181819;
		overflow: hidden;
	}

	.watchlist-header {
		padding: 10px 12px;
		border-bottom: 1px solid #262629;
		color: #d1d2d7;
		font-size: 13px;
		font-weight: 600;
	}

	.watchlist-row {
		position: relative;
		padding: 14px 10px;
		border-bottom: 1px solid #232326;
		font-size: 13px;
		gap: 12px;
		cursor: pointer;
	}

	.watchlist-row:last-child {
		border-bottom: none;
	}

	.selected-row {
		background: rgba(43, 88, 199, 0.08);
	}

	.watchlist-main {
		width: 100%;
		gap: 12px;
	}

	.watchlist-labels {
		flex-direction: column;
		align-items: start;
		gap: 4px;
	}

	.watchlist-labels strong,
	.watch-price {
		color: #d06451;
		font-weight: 600;
	}

	.watchlist-labels span {
		color: #72747a;
		font-size: 11px;
	}

	.watchlist-stats {
		gap: 14px;
		color: #8f9095;
		text-align: right;
	}

	.watchlist-actions {
		position: absolute;
		right: 10px;
		top: 50%;
		display: flex;
		gap: 6px;
		opacity: 0;
		transform: translateY(-50%);
		pointer-events: none;
		transition: opacity 160ms ease;
	}

	.watchlist-row:hover .watchlist-actions,
	.watchlist-row:focus-within .watchlist-actions,
	.selected-row .watchlist-actions {
		opacity: 1;
		pointer-events: auto;
	}

	.watchlist-row:hover .watchlist-stats,
	.watchlist-row:focus-within .watchlist-stats,
	.selected-row .watchlist-stats {
		opacity: 0.18;
	}

	.watchlist-actions button {
		height: 26px;
		border: 1px solid #2d3241;
		border-radius: 3px;
		padding: 0 10px;
		color: #e6e8ed;
		cursor: pointer;
	}

	.buy-btn {
		background: #4f7df7;
	}

	.sell-btn {
		background: #d67d4c;
	}

	.chart-btn {
		background: #202530;
	}

	.watchlist-empty {
		padding: 16px 12px;
		color: #75767b;
		font-size: 13px;
	}

	.watchlist-footer {
		align-self: end;
		padding: 14px 4px 0;
		border-top: 1px solid #242426;
		color: #707177;
	}

	.page-indicators {
		display: flex;
		gap: 16px;
	}

	.page-indicators button {
		position: relative;
		padding: 8px 0 0;
		color: #717278;
		font-size: 12px;
	}

	.page-indicators button.active {
		color: #d17757;
	}

	.page-indicators button.active::before {
		content: '';
		position: absolute;
		top: -14px;
		left: 50%;
		width: 40px;
		height: 3px;
		background: #d17757;
		transform: translateX(-50%);
	}

	.footer-icons {
		display: flex;
		gap: 8px;
	}

	.footer-icons span {
		width: 12px;
		height: 12px;
		border: 1px solid #64666b;
		border-radius: 2px;
	}

	.dashboard {
		padding: 0 24px 28px;
	}

	.dashboard-head {
		padding: 20px 0 14px;
		border-bottom: 1px solid #252528;
	}

	h1,
	h2,
	p {
		margin: 0;
	}

	h1 {
		font-size: 19px;
		font-weight: 500;
		color: #d5d6db;
	}

	h2 {
		font-size: 18px;
		font-weight: 500;
		color: #c7c8cc;
	}

	.dashboard-head p {
		margin-top: 6px;
		color: #74767c;
		font-size: 13px;
	}

	.section {
		padding: 30px 0 0;
		border-bottom: 1px solid #252528;
	}

	.chart-stage {
		padding-bottom: 30px;
	}

	.chart-view-tabs {
		display: flex;
		gap: 26px;
		margin-bottom: 18px;
	}

	.chart-view-tabs button,
	.interval-tabs button,
	.toolbar-right button {
		padding: 0;
		border: none;
		background: transparent;
		color: #8f9197;
		cursor: pointer;
	}

	.chart-view-tabs button {
		padding-bottom: 10px;
		font-size: 14px;
	}

	.chart-view-tabs button.active {
		color: #d17a55;
		border-bottom: 2px solid #d17a55;
	}

	.chart-workspace {
		display: grid;
		grid-template-columns: minmax(0, 1fr) 320px;
		gap: 24px;
	}

	.chart-panel,
	.chart-sidebar {
		display: grid;
		gap: 16px;
	}

	.chart-toolbar,
	.toolbar-left,
	.chart-stats,
	.chart-meta {
		display: flex;
		align-items: center;
	}

	.chart-toolbar,
	.chart-stats {
		justify-content: space-between;
	}

	.toolbar-left {
		gap: 18px;
	}

	.selected-symbol {
		display: grid;
		gap: 4px;
	}

	.selected-symbol span {
		color: #7a7d85;
		font-size: 12px;
	}

	.interval-tabs,
	.toolbar-right {
		display: flex;
		align-items: center;
		gap: 14px;
	}

	.interval-tabs button,
	.toolbar-right button {
		font-size: 12px;
	}

	.interval-tabs button.active,
	.toolbar-right button:hover {
		color: #d17a55;
	}

	.chart-stats {
		gap: 14px;
	}

	.stat-pill {
		min-width: 110px;
		padding: 10px 14px;
		border-radius: 4px;
		display: grid;
		gap: 3px;
	}

	.stat-pill span {
		font-size: 18px;
		font-weight: 600;
		color: #f5f7fb;
	}

	.stat-pill strong {
		font-size: 11px;
		font-weight: 700;
		letter-spacing: 0.08em;
	}

	.buy {
		background: #4372e8;
	}

	.sell {
		background: #d77a4f;
	}

	.chart-meta {
		gap: 24px;
		margin-left: auto;
	}

	.chart-meta p {
		display: grid;
		gap: 4px;
	}

	.chart-meta span,
	.health-state p {
		color: #777a82;
		font-size: 12px;
	}

	.health-state {
		display: grid;
		gap: 10px;
	}

	.compact {
		align-content: start;
	}

	.margin-card {
		display: grid;
		gap: 18px;
	}

	.margin-title {
		gap: 10px;
		color: #d2d3d7;
	}

	.dot-icon {
		width: 12px;
		height: 12px;
		border-radius: 50%;
		background: #b9bbc1;
	}

	.dot-icon.hollow {
		background: transparent;
		border: 1px solid #b9bbc1;
	}

	.primary-metric {
		min-width: 142px;
		display: grid;
		gap: 4px;
	}

	.primary-metric strong {
		font-size: 42px;
		font-weight: 400;
		letter-spacing: -0.02em;
		color: #dadbe0;
	}

	.primary-metric span,
	.secondary-metrics span,
	.holdings-pnl p,
	.holdings-metrics span,
	.chart-axis span,
	.analysis-item p {
		color: #717278;
		font-size: 12px;
	}

	.vertical-rule {
		width: 1px;
		align-self: stretch;
		background: #29292c;
	}

	.secondary-metrics,
	.holdings-metrics,
	.analysis-list {
		display: grid;
	}

	.secondary-metrics,
	.holdings-metrics {
		gap: 12px;
		min-width: 220px;
	}

	.secondary-metrics strong,
	.holdings-metrics strong,
	.allocation-footer strong,
	.analysis-item strong,
	.stream-chip strong {
		color: #d3d4d8;
		font-weight: 500;
	}

	.statement-link {
		width: fit-content;
		padding: 0;
		border: none;
		background: transparent;
		color: #4f84ff;
		font-size: 12px;
		cursor: pointer;
	}

	.holdings-section {
		padding-bottom: 28px;
	}

	.section-title {
		gap: 10px;
		color: #cfd0d5;
		margin-bottom: 14px;
	}

	.panel-mark {
		width: 12px;
		height: 12px;
		border-left: 2px solid #9fa1a8;
		border-top: 2px solid #9fa1a8;
		transform: rotate(45deg);
	}

	.holdings-summary {
		max-width: 720px;
		gap: 28px;
		margin-bottom: 18px;
	}

	.holdings-pnl {
		display: grid;
		grid-template-columns: auto auto;
		align-items: end;
		gap: 6px 10px;
	}

	.holdings-pnl strong {
		font-size: 38px;
		font-weight: 400;
		letter-spacing: -0.02em;
		grid-column: 1 / 2;
	}

	.holdings-pnl span {
		font-size: 21px;
		align-self: end;
		padding-bottom: 6px;
	}

	.holdings-pnl p {
		grid-column: 1 / -1;
	}

	.positive {
		color: #67a769;
	}

	.negative {
		color: #bf6d62;
	}

	.allocation-track {
		height: 45px;
		display: flex;
		overflow: hidden;
		margin: 10px 0 10px;
		background: #202024;
	}

	.allocation-track span {
		height: 100%;
		display: block;
	}

	.empty-allocation {
		width: 100%;
		background: #242428;
	}

	.allocation-footer strong {
		font-size: 15px;
		font-weight: 600;
	}

	.legend {
		gap: 24px;
		color: #77787d;
		font-size: 12px;
	}

	.legend-item {
		display: flex;
		align-items: center;
		gap: 6px;
	}

	.legend-item i {
		width: 10px;
		height: 10px;
		display: inline-block;
		border: 1px solid #45464c;
		border-radius: 50%;
	}

	.legend-item.active i {
		border-color: #5a84ff;
		box-shadow: inset 0 0 0 2px #5a84ff;
	}

	.lower-grid {
		display: grid;
		grid-template-columns: minmax(0, 1.05fr) 0.95fr;
		gap: 36px;
		padding-bottom: 0;
		border-bottom: none;
	}

	.overview-panel,
	.positions-panel {
		padding: 10px 0 0;
	}

	.chart-legend {
		margin: 0 0 8px 16px;
		color: #9ea0a6;
		font-size: 11px;
		position: relative;
	}

	.chart-legend::before {
		content: '';
		position: absolute;
		left: -10px;
		top: 4px;
		width: 6px;
		height: 6px;
		background: #5a84ff;
	}

	.overview-chart {
		max-width: 460px;
	}

	.overview-chart svg {
		display: block;
		width: 100%;
		height: auto;
	}

	.grid-line {
		stroke: #242528;
		stroke-width: 1;
		fill: none;
	}

	.market-line {
		fill: none;
		stroke: #5583ff;
		stroke-width: 3;
		stroke-linecap: round;
		stroke-linejoin: round;
	}

	.chart-axis {
		display: flex;
		justify-content: space-around;
		margin-top: -6px;
	}

	.positions-panel {
		display: grid;
		align-content: start;
		gap: 14px;
	}

	.analysis-list {
		gap: 12px;
	}

	.analysis-item {
		gap: 10px;
		color: #88898e;
	}

	.position-marker {
		width: 2px;
		height: 13px;
		background: #d57a56;
	}

	.stream-chip {
		width: fit-content;
		gap: 12px;
		padding: 7px 10px;
		border: 1px solid #2b2b2e;
		border-radius: 2px;
		background: #171719;
		color: #7e8086;
		font-size: 12px;
		text-transform: capitalize;
	}

	.status-live {
		color: #71bc80;
	}

	.status-badge {
		width: fit-content;
		padding: 6px 10px;
		border: 1px solid #2d3241;
		background: #171719;
		text-transform: capitalize;
	}

	@media (max-width: 1240px) {
		.topbar {
			grid-template-columns: 1fr;
			height: auto;
		}

		.ticker-strip,
		.workspace-switcher,
		.profile-actions {
			border-right: none;
			border-bottom: 1px solid #262628;
			padding: 10px 14px;
		}

		.main-nav {
			justify-content: flex-start;
			padding: 8px 10px;
			flex-wrap: wrap;
		}

		.content-shell {
			grid-template-columns: 1fr;
		}

		.marketwatch {
			border-right: none;
			border-bottom: 1px solid #242426;
		}

		.chart-workspace {
			grid-template-columns: 1fr;
		}
	}

	@media (max-width: 820px) {
		.dashboard {
			padding: 0 14px 22px;
		}

		.lower-grid {
			grid-template-columns: 1fr;
			gap: 24px;
		}

		.margin-body,
		.holdings-summary,
		.allocation-footer {
			flex-direction: column;
			align-items: start;
		}

		.chart-toolbar,
		.chart-stats,
		.toolbar-left,
		.chart-meta {
			flex-direction: column;
			align-items: start;
		}

		.vertical-rule {
			width: 100%;
			height: 1px;
		}

		.legend {
			flex-wrap: wrap;
			gap: 12px;
		}
	}

	@media (max-width: 640px) {
		.watchlist-row,
		.watchlist-main,
		.secondary-metrics p,
		.holdings-metrics p {
			flex-direction: column;
			align-items: start;
		}

		.watchlist-stats {
			width: 100%;
			justify-content: space-between;
		}

		.watchlist-actions {
			position: static;
			opacity: 1;
			transform: none;
			pointer-events: auto;
		}
	}
</style>
