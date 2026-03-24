import { groupBy, sumBy } from "../../../shared/utils/src/index.js";

const SECTOR_MAP = Object.freeze({
  INFY: "IT",
  TCS: "IT",
  RELIANCE: "Energy",
  HDFCBANK: "Banking",
  BTCUSDT: "Crypto"
});

export function createPortfolioModule({ repositories, logger }) {
  return {
    getSummary() {
      const filledOrders = repositories.orders
        .list()
        .filter((order) => order.status === "filled");

      const positionsBySymbol = groupBy(filledOrders, (order) => order.symbol);
      const positions = Object.entries(positionsBySymbol).map(([symbol, orders]) => {
        const signedQuantity = sumBy(orders, (order) =>
          order.side === "buy" ? order.quantity : -order.quantity
        );
        const averagePrice =
          sumBy(orders, (order) => order.quantity * order.price) /
          Math.max(sumBy(orders, (order) => order.quantity), 1);

        return {
          symbol,
          sector: SECTOR_MAP[symbol] ?? "Other",
          quantity: signedQuantity,
          averagePrice: Number(averagePrice.toFixed(2))
        };
      });

      const sectorDistribution = groupBy(positions, (position) => position.sector);
      const summary = {
        holdings: positions,
        sectors: Object.entries(sectorDistribution).map(([sector, sectorPositions]) => ({
          sector,
          symbols: sectorPositions.map((position) => position.symbol)
        })),
        totalExposure: Number(
          sumBy(positions, (position) => position.quantity * position.averagePrice).toFixed(2)
        ),
        log: logger.info("Portfolio summary generated", { holdings: positions.length })
      };

      repositories.portfolioSnapshots.insert(summary);
      return summary;
    }
  };
}
