function average(values) {
  return values.reduce((total, value) => total + value, 0) / values.length;
}

function last(values) {
  return values[values.length - 1];
}

function evaluateSma(candles, period = 3) {
  if (candles.length < period) {
    return { signal: "hold", confidence: 0 };
  }

  const closes = candles.map((candle) => candle.close);
  const baseline = average(closes.slice(-period));
  const latest = last(closes);

  return latest >= baseline
    ? { signal: "buy", confidence: 0.65 }
    : { signal: "sell", confidence: 0.65 };
}

function evaluateRsi(candles, period = 3) {
  if (candles.length <= period) {
    return { signal: "hold", confidence: 0 };
  }

  let gains = 0;
  let losses = 0;

  for (let index = candles.length - period; index < candles.length; index += 1) {
    const change = candles[index].close - candles[index - 1].close;
    if (change >= 0) {
      gains += change;
    } else {
      losses += Math.abs(change);
    }
  }

  if (losses === 0) {
    return { signal: "sell", confidence: 0.7 };
  }

  const rs = gains / losses;
  const rsi = 100 - 100 / (1 + rs);

  if (rsi <= 30) {
    return { signal: "buy", confidence: 0.72 };
  }

  if (rsi >= 70) {
    return { signal: "sell", confidence: 0.72 };
  }

  return { signal: "hold", confidence: 0.45 };
}

function evaluateWeighted(candles, weights = { sma: 0.5, rsi: 0.5 }) {
  const sma = evaluateSma(candles);
  const rsi = evaluateRsi(candles);
  const score =
    (sma.signal === "buy" ? 1 : sma.signal === "sell" ? -1 : 0) * weights.sma +
    (rsi.signal === "buy" ? 1 : rsi.signal === "sell" ? -1 : 0) * weights.rsi;

  if (score > 0.2) {
    return { signal: "buy", confidence: 0.68 };
  }

  if (score < -0.2) {
    return { signal: "sell", confidence: 0.68 };
  }

  return { signal: "hold", confidence: 0.4 };
}

export function createStrategyRegistry() {
  const definitions = [
    { code: "sma", label: "Simple Moving Average", defaultParams: { period: 3 } },
    { code: "rsi", label: "Relative Strength Index", defaultParams: { period: 3 } },
    {
      code: "custom-weighted",
      label: "Weighted Composite",
      defaultParams: { weights: { sma: 0.6, rsi: 0.4 } }
    }
  ];

  return {
    list() {
      return definitions;
    },
    evaluate({ strategyCode, candles, params = {} }) {
      if (strategyCode === "sma") {
        return evaluateSma(candles, params.period);
      }

      if (strategyCode === "rsi") {
        return evaluateRsi(candles, params.period);
      }

      if (strategyCode === "custom-weighted") {
        return evaluateWeighted(candles, params.weights);
      }

      throw new Error(`Unknown strategy: ${strategyCode}`);
    }
  };
}
