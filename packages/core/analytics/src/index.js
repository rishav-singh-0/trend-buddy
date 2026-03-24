import { REALTIME_EVENTS } from "../../../shared/contracts/src/index.js";

export function createAnalyticsModule({ repositories, logger }) {
  return {
    async analyze({ symbol, fundamentalsScore = 0.6, sentimentScore = 0.55 }) {
      const advisoryScore = Number(((fundamentalsScore + sentimentScore) / 2).toFixed(2));
      const insight = {
        symbol,
        advisoryOnly: true,
        advisoryScore,
        summary:
          advisoryScore >= 0.65
            ? "Constructive outlook; keep strategy and risk checks in the loop."
            : "Mixed outlook; rely on confirmation from strategy and risk modules.",
        event: REALTIME_EVENTS.analyticsReady,
        log: logger.info("Analytics report generated", { symbol, advisoryScore })
      };

      repositories.analytics.insert(insight);
      return insight;
    }
  };
}
