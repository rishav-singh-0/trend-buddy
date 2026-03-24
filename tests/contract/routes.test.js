import test from "node:test";
import assert from "node:assert/strict";

import { DOMAIN_ROUTES, createRouteTable } from "../../packages/shared/contracts/src/index.js";

test("domain routes cover the planned surface area", () => {
  const routes = createRouteTable();

  assert.equal(routes.length, 6);
  assert.deepEqual(routes.map((route) => route.path), Object.values(DOMAIN_ROUTES));
});
