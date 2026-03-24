import test from "node:test";
import assert from "node:assert/strict";

import { createApplication } from "../../apps/api/src/app.js";
import { DOMAIN_ROUTES } from "../../packages/shared/contracts/src/index.js";

test("ingest -> backtest -> place order -> portfolio -> analytics flow stays connected", async () => {
  const app = createApplication();

  await app.handleRequest({
    route: DOMAIN_ROUTES.marketData,
    method: "POST",
    payload: {
      provider: "yfinance",
      symbol: "INFY",
      interval: "1d"
    }
  });

  const backtest = await app.handleRequest({
    route: DOMAIN_ROUTES.backtests,
    method: "POST",
    payload: {
      symbol: "INFY",
      strategyCode: "sma",
      interval: "1d"
    }
  });

  const order = await app.handleRequest({
    route: DOMAIN_ROUTES.orders,
    method: "POST",
    payload: {
      broker: "zerodha",
      symbol: "INFY",
      side: "buy",
      quantity: 3,
      price: 207
    }
  });

  const portfolio = await app.handleRequest({
    route: DOMAIN_ROUTES.portfolio,
    method: "GET"
  });

  const analytics = await app.handleRequest({
    route: DOMAIN_ROUTES.analytics,
    method: "POST",
    payload: {
      symbol: "INFY",
      fundamentalsScore: 0.72,
      sentimentScore: 0.64
    }
  });

  assert.equal(backtest.data.symbol, "INFY");
  assert.equal(order.data.status, "filled");
  assert.equal(portfolio.data.holdings[0].symbol, "INFY");
  assert.equal(analytics.data.advisoryOnly, true);
});
