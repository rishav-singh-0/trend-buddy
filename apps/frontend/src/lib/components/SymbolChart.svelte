<script lang="ts">
	import { browser } from '$app/environment';
	import { getApiBaseUrl } from '$lib/api';
	import type { MarketCandle, MarketCandlesResponse } from '$lib/types';
	import { onDestroy, onMount } from 'svelte';

	export let symbol: string;
	export let activePrice: number | null = null;
	export let interval = '1D';
	export let height = 560;

	let container: HTMLDivElement;
	let chartApi: any = null;
	let candlestickSeries: any = null;
	let volumeSeries: any = null;
	let resizeObserver: ResizeObserver | null = null;
	let chartLibrary: any = null;
	let loading = false;
	let error = '';
	let candles: MarketCandle[] = [];
	let lastLoadedKey = '';

	async function ensureChart() {
		if (!browser || !container || chartApi) {
			return;
		}

		chartLibrary = await import('lightweight-charts');
		const { createChart, CandlestickSeries, HistogramSeries, ColorType } = chartLibrary;

		chartApi = createChart(container, {
			autoSize: true,
			height,
			layout: {
				background: { type: ColorType.Solid, color: '#171b26' },
				textColor: '#848995'
			},
			grid: {
				vertLines: { color: '#232836' },
				horzLines: { color: '#232836' }
			},
			rightPriceScale: {
				borderColor: '#262c3c'
			},
			timeScale: {
				borderColor: '#262c3c',
				timeVisible: true
			},
			crosshair: {
				vertLine: { color: '#394256' },
				horzLine: { color: '#394256' }
			}
		});

		candlestickSeries = chartApi.addSeries(CandlestickSeries, {
			upColor: '#26a69a',
			downColor: '#ef5350',
			borderVisible: false,
			wickUpColor: '#26a69a',
			wickDownColor: '#ef5350',
			priceLineVisible: activePrice !== null,
			lastValueVisible: true
		});

		volumeSeries = chartApi.addSeries(HistogramSeries, {
			priceFormat: { type: 'volume' },
			priceScaleId: 'volume',
			color: '#325ef1'
		});

		chartApi.priceScale('volume').applyOptions({
			scaleMargins: {
				top: 0.78,
				bottom: 0
			}
		});

		resizeObserver = new ResizeObserver(() => {
			chartApi?.timeScale().fitContent();
		});
		resizeObserver.observe(container);
	}

	async function loadCandles() {
		const requestKey = `${symbol}:${interval}`;
		if (!browser || !symbol || requestKey === lastLoadedKey) {
			return;
		}

		loading = true;
		error = '';

		try {
			await ensureChart();
			const response = await fetch(
				`${getApiBaseUrl()}/market-data/candles?symbol=${encodeURIComponent(symbol)}&interval=${encodeURIComponent(interval)}&provider=yfinance`
			);
			if (!response.ok) {
				throw new Error(`Candles request failed with ${response.status}`);
			}

			const payload = (await response.json()) as MarketCandlesResponse;
			candles = payload.candles;
			candlestickSeries?.setData(
				candles.map((candle) => ({
					time: candle.time,
					open: candle.open,
					high: candle.high,
					low: candle.low,
					close: candle.close
				}))
			);
			volumeSeries?.setData(
				candles.map((candle) => ({
					time: candle.time,
					value: candle.volume,
					color: candle.close >= candle.open ? 'rgba(38, 166, 154, 0.55)' : 'rgba(239, 83, 80, 0.55)'
				}))
			);
			chartApi?.timeScale().fitContent();
			lastLoadedKey = requestKey;
		} catch (caughtError) {
			error = caughtError instanceof Error ? caughtError.message : 'Unable to load candles.';
		} finally {
			loading = false;
		}
	}

	function updatePriceLine() {
		if (!candlestickSeries) {
			return;
		}

		candlestickSeries.applyOptions({
			priceLineVisible: activePrice !== null
		});
	}

	onMount(() => {
		loadCandles();
	});

	onDestroy(() => {
		resizeObserver?.disconnect();
		chartApi?.remove();
	});

	$: if (browser && symbol) {
		loadCandles();
	}

	$: if (browser && chartApi) {
		updatePriceLine();
	}
</script>

<div class="chart-shell" style={`height:${height}px`}>
	<div bind:this={container} class="chart-host"></div>

	{#if loading}
		<div class="chart-state">Loading candles for {symbol}...</div>
	{:else if error}
		<div class="chart-state error">{error}</div>
	{/if}
</div>

<style>
	.chart-shell {
		position: relative;
		width: 100%;
		border: 1px solid #232836;
		background: #171b26;
	}

	.chart-host {
		width: 100%;
		height: 100%;
	}

	.chart-state {
		position: absolute;
		top: 14px;
		right: 14px;
		padding: 6px 10px;
		background: rgba(12, 15, 22, 0.88);
		border: 1px solid #293144;
		color: #9ca3af;
		font-size: 12px;
	}

	.error {
		color: #e58a84;
	}
</style>
