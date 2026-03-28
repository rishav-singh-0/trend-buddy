import { LineSeries, LineStyle, createChart } from 'lightweight-charts';

import { PROBE_CONFIG, PROBE_OPTIONS } from '@/utils/probes';

function hexToRgba(hex, alpha) {
  const sanitizedHex = hex.replace('#', '');
  const value = Number.parseInt(sanitizedHex, 16);
  const red = (value >> 16) & 255;
  const green = (value >> 8) & 255;
  const blue = value & 255;

  return `rgba(${red}, ${green}, ${blue}, ${alpha})`;
}

export class ChartManager {
  constructor(options = {}) {
    this.chart = null;
    this.series = new Map();
    this.container = null;

    this.defaultOptions = {
      layout: {
        textColor: '#d1d4dc',
        background: { type: 'solid', color: 'transparent' },
        panes: {
          separatorColor: 'rgba(96, 96, 96, 0.2)',
        },
      },
      grid: {
        vertLines: { color: 'rgba(255, 255, 255, 0.04)' },
        horzLines: { color: 'rgba(255, 255, 255, 0.06)' },
      },
      leftPriceScale: {
        visible: false,
      },
      rightPriceScale: {
        borderColor: 'rgba(255, 255, 255, 0.08)',
      },
      crosshair: {
        vertLine: {
          color: 'rgba(255, 255, 255, 0.18)',
        },
        horzLine: {
          color: 'rgba(255, 255, 255, 0.18)',
        },
      },
      autoSize: true,
      ...options,
    };

    this.timeScaleOptions = {
      timeVisible: true,
      secondsVisible: true,
      rightOffset: 4,
      borderColor: 'rgba(255, 255, 255, 0.08)',
    };
  }

  init(containerElement) {
    this.container = containerElement;

    this.chart = createChart(containerElement, this.defaultOptions);
    this.chart.timeScale().applyOptions(this.timeScaleOptions);
  }

  syncSeries(records, activeKey) {
    if (!this.chart) {
      return;
    }

    let hasSamples = false;

    PROBE_OPTIONS.forEach((option) => {
      const key = option.value;
      const data = records[key]?.samples ?? [];

      if (data.length > 0) {
        hasSamples = true;
      }

      this.addSeries(key, data, this.buildSeriesOptions(key, activeKey));
    });

    if (hasSamples) {
      this.chart.timeScale().fitContent();
    }
  }

  addSeries(key, data, seriesOptions) {
    if (this.series.has(key)) {
      const existingSeries = this.series.get(key);
      existingSeries.setData(data);
      existingSeries.applyOptions(seriesOptions);
      return existingSeries;
    }

    const lineSeries = this.chart.addSeries(LineSeries, seriesOptions);
    lineSeries.setData(data);
    this.series.set(key, lineSeries);

    return lineSeries;
  }

  buildSeriesOptions(key, activeKey) {
    const accent = PROBE_CONFIG[key].accent;
    const isActive = key === activeKey;

    return {
      color: isActive ? accent : hexToRgba(accent, 0.55),
      lineWidth: isActive ? 3 : 2,
      lineStyle: isActive ? LineStyle.Solid : LineStyle.Dashed,
      crosshairMarkerVisible: isActive,
      crosshairMarkerRadius: 4,
      crosshairMarkerBorderColor: accent,
      crosshairMarkerBackgroundColor: accent,
      lastValueVisible: true,
      priceLineVisible: isActive,
      priceLineColor: hexToRgba(accent, 0.75),
      priceFormat: {
        type: 'price',
        precision: 0,
        minMove: 1,
      },
    };
  }

  destroy() {
    if (!this.chart) {
      return;
    }

    this.chart.remove();
    this.chart = null;
    this.container = null;
    this.series.clear();
  }
}
