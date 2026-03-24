export function createRiskModule({ repositories, config }) {
  return {
    assess(order) {
      const openOrdersValue = repositories.orders
        .list()
        .filter((entry) => entry.status === "filled")
        .reduce((total, entry) => total + entry.quantity * entry.price, 0);

      const orderValue = order.quantity * order.price;
      const totalExposure = openOrdersValue + orderValue;
      const approved = orderValue <= config.risk.maxOrderValue;

      return {
        approved,
        reason: approved ? "within_limit" : "order_value_exceeds_limit",
        orderValue,
        totalExposure
      };
    }
  };
}
