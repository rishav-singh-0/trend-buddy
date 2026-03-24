export function createGrowwBroker() {
  return {
    name: "groww",
    async placeOrder({ symbol, side, quantity, price }) {
      return {
        broker: "groww",
        symbol,
        side,
        quantity,
        price,
        status: "filled",
        brokerOrderId: `groww-${symbol}-${Date.now()}`
      };
    }
  };
}
