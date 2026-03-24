import { DOMAIN_ROUTES } from "../../../packages/shared/contracts/src/index.js";

export function createWebAppShell() {
  return {
    navigation: [
      { label: "Market Data", route: DOMAIN_ROUTES.marketData },
      { label: "Strategies", route: DOMAIN_ROUTES.strategies },
      { label: "Backtests", route: DOMAIN_ROUTES.backtests },
      { label: "Orders", route: DOMAIN_ROUTES.orders },
      { label: "Portfolio", route: DOMAIN_ROUTES.portfolio },
      { label: "Analytics", route: DOMAIN_ROUTES.analytics }
    ],
    dashboard: {
      charts: ["candlestick", "pnl", "sector-allocation"],
      tools: ["sip-calculator", "pattern-detector", "strategy-builder"],
      realtimePanels: ["price-ticker", "order-status", "risk-summary"]
    }
  };
}
