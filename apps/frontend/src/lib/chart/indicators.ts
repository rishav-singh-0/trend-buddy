import type { MarketCandle } from '$lib/types';

export type ChartIndicatorId = 'sma20' | 'sma50' | 'ema21';

export type ChartIndicatorDefinition = {
	id: ChartIndicatorId;
	name: string;
	shortLabel: string;
	description: string;
	color: string;
	length: number;
	method: 'sma' | 'ema';
};

export type IndicatorPoint = {
	time: number;
	value: number;
};

export const CHART_INDICATORS: ChartIndicatorDefinition[] = [
	{
		id: 'sma20',
		name: 'Simple Moving Average 20',
		shortLabel: 'SMA 20',
		description: 'Short-term trend overlay for fast momentum checks.',
		color: '#5b8cff',
		length: 20,
		method: 'sma'
	},
	{
		id: 'sma50',
		name: 'Simple Moving Average 50',
		shortLabel: 'SMA 50',
		description: 'Medium-term trend baseline for swing context.',
		color: '#ffb347',
		length: 50,
		method: 'sma'
	},
	{
		id: 'ema21',
		name: 'Exponential Moving Average 21',
		shortLabel: 'EMA 21',
		description: 'Responsive trend overlay for pullback timing.',
		color: '#5fd0a5',
		length: 21,
		method: 'ema'
	}
];

export const DEFAULT_CHART_INDICATORS: ChartIndicatorId[] = ['sma20', 'ema21'];

export function getChartIndicatorById(id: string): ChartIndicatorDefinition | undefined {
	return CHART_INDICATORS.find((indicator) => indicator.id === id);
}

export function buildIndicatorSeries(
	indicator: ChartIndicatorDefinition,
	candles: MarketCandle[]
): IndicatorPoint[] {
	if (!candles.length) {
		return [];
	}

	return indicator.method === 'ema'
		? buildExponentialMovingAverage(candles, indicator.length)
		: buildSimpleMovingAverage(candles, indicator.length);
}

function buildSimpleMovingAverage(candles: MarketCandle[], length: number): IndicatorPoint[] {
	let rollingTotal = 0;
	const points: IndicatorPoint[] = [];

	for (let index = 0; index < candles.length; index += 1) {
		rollingTotal += candles[index].close;

		if (index >= length) {
			rollingTotal -= candles[index - length].close;
		}

		if (index >= length - 1) {
			points.push({
				time: candles[index].time,
				value: rollingTotal / length
			});
		}
	}

	return points;
}

function buildExponentialMovingAverage(candles: MarketCandle[], length: number): IndicatorPoint[] {
	const smoothingFactor = 2 / (length + 1);
	const points: IndicatorPoint[] = [];

	if (candles.length < length) {
		return points;
	}

	let seed = 0;
	for (let index = 0; index < length; index += 1) {
		seed += candles[index].close;
	}

	let previousValue = seed / length;
	points.push({
		time: candles[length - 1].time,
		value: previousValue
	});

	for (let index = length; index < candles.length; index += 1) {
		previousValue = candles[index].close * smoothingFactor + previousValue * (1 - smoothingFactor);
		points.push({
			time: candles[index].time,
			value: previousValue
		});
	}

	return points;
}
