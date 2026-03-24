export function createZerodhaBroker() {
  return {
    name: "zerodha",
    async placeOrder({ symbol, side, quantity, price }) {
      return {
        broker: "zerodha",
        symbol,
        side,
        quantity,
        price,
        status: "filled",
        brokerOrderId: `zerodha-${symbol}-${Date.now()}`
      };
    }
  };
}
