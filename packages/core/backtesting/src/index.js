export function createBacktestingModule({ repositories, strategies, logger }) {
  return {
    async run({ symbol, strategyCode, params = {}, interval = "1d" }) {
      const candles = repositories
        .listCandlesBySymbol(symbol)
        .filter((candle) => candle.interval === interval);

      const evaluation = strategies.evaluate({
        strategyCode,
        candles,
        params
      });

      const latestClose = candles.at(-1)?.close ?? 0;
      const firstClose = candles.at(0)?.close ?? latestClose;
      const grossMove = latestClose - firstClose;
      const direction = evaluation.signal === "sell" ? -1 : evaluation.signal === "buy" ? 1 : 0;
      const netPnl = Number((grossMove * direction).toFixed(2));

      const result = {
        symbol,
        interval,
        strategyCode,
        metrics: {
          candleCount: candles.length,
          netPnl,
          maxDrawdown: Number(Math.abs(grossMove * 0.35).toFixed(2))
        },
        evaluation,
        log: logger.info("Completed backtest", { symbol, strategyCode })
      };

      repositories.backtests.insert(result);
      return result;
    }
  };
}
