export function createBinanceBroker() {
  return {
    name: "binance",
    async placeOrder({ symbol, side, quantity, price }) {
      return {
        broker: "binance",
        symbol,
        side,
        quantity,
        price,
        status: "filled",
        brokerOrderId: `binance-${symbol}-${Date.now()}`
      };
    }
  };
}
