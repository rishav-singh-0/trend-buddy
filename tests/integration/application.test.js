import test from "node:test";
import assert from "node:assert/strict";

import { createApplication } from "../../apps/api/src/app.js";
import { DOMAIN_ROUTES } from "../../packages/shared/contracts/src/index.js";

test("application composes all planned modules and routes", async () => {
  const app = createApplication();
  const marketData = await app.handleRequest({
    route: DOMAIN_ROUTES.marketData,
    method: "GET"
  });

  assert.deepEqual(Object.keys(app.modules).sort(), [
    "analytics",
    "backtesting",
    "marketData",
    "orders",
    "portfolio",
    "risk",
    "strategies"
  ]);
  assert.equal(marketData.data.providers.length, 3);
  assert.equal(Object.keys(app.routes).length, 6);
});
