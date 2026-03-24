import { REALTIME_EVENTS } from "../../../shared/contracts/src/index.js";

export function createOrderExecutionModule({ repositories, providers, risk, logger }) {
  return {
    async placeOrder({ broker, symbol, side, quantity, price }) {
      const adapter = providers[broker];
      if (!adapter) {
        throw new Error(`Unsupported broker provider: ${broker}`);
      }

      const assessment = risk.assess({ symbol, side, quantity, price });
      if (!assessment.approved) {
        return {
          status: "rejected",
          reason: assessment.reason,
          risk: assessment
        };
      }

      const execution = await adapter.placeOrder({ symbol, side, quantity, price });
      const record = {
        ...execution,
        event: REALTIME_EVENTS.orderUpdated,
        placedAt: new Date().toISOString()
      };

      repositories.orders.insert(record);

      return {
        ...record,
        log: logger.info("Order executed", { broker, symbol, side, quantity })
      };
    }
  };
}
