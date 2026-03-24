import { createAnalyticsModule } from "../../../packages/core/analytics/src/index.js";
import { createBacktestingModule } from "../../../packages/core/backtesting/src/index.js";
import { createMarketDataModule } from "../../../packages/core/market-data/src/index.js";
import { createOrderExecutionModule } from "../../../packages/core/orders/src/index.js";
import { createPortfolioModule } from "../../../packages/core/portfolio/src/index.js";
import { createRiskModule } from "../../../packages/core/risk/src/index.js";
import { createStrategyRegistry } from "../../../packages/core/strategies/src/index.js";
import { createInMemoryCache } from "../../../packages/data/cache/src/index.js";
import { createInMemoryRepositories } from "../../../packages/data/repositories/src/index.js";
import { createBinanceBroker } from "../../../packages/integrations/brokers/binance/src/index.js";
import { createGrowwBroker } from "../../../packages/integrations/brokers/groww/src/index.js";
import { createZerodhaBroker } from "../../../packages/integrations/brokers/zerodha/src/index.js";
import { createAlphaVantageProvider } from "../../../packages/integrations/market-data/alpha-vantage/src/index.js";
import { createNseProvider } from "../../../packages/integrations/market-data/nse/src/index.js";
import { createYFinanceProvider } from "../../../packages/integrations/market-data/yfinance/src/index.js";
import { loadConfig } from "../../../packages/shared/config/src/index.js";
import { DOMAIN_ROUTES, createApiResponse } from "../../../packages/shared/contracts/src/index.js";
import { createLogger } from "../../../packages/shared/logging/src/index.js";

export function createApplication({ configOverrides = {} } = {}) {
  const config = loadConfig(configOverrides);
  const logger = createLogger({ service: "api" });
  const repositories = createInMemoryRepositories();
  const cache = createInMemoryCache();
  const strategies = createStrategyRegistry();

  const marketDataProviders = {
    nse: createNseProvider(),
    yfinance: createYFinanceProvider(),
    "alpha-vantage": createAlphaVantageProvider()
  };

  const brokerProviders = {
    zerodha: createZerodhaBroker(),
    groww: createGrowwBroker(),
    binance: createBinanceBroker()
  };

  const risk = createRiskModule({ repositories, config });
  const marketData = createMarketDataModule({
    repositories,
    providers: marketDataProviders,
    cache,
    logger
  });
  const backtesting = createBacktestingModule({
    repositories,
    strategies,
    logger
  });
  const portfolio = createPortfolioModule({ repositories, logger });
  const orders = createOrderExecutionModule({
    repositories,
    providers: brokerProviders,
    risk,
    logger
  });
  const analytics = createAnalyticsModule({ repositories, logger });

  const routes = {
    [DOMAIN_ROUTES.marketData]: {
      GET: async () =>
        createApiResponse({
          providers: marketData.listProviders(),
          supportedIntervals: config.marketData.supportedIntervals
        }),
      POST: async (payload) => createApiResponse(await marketData.ingestCandles(payload))
    },
    [DOMAIN_ROUTES.strategies]: {
      GET: async () => createApiResponse({ strategies: strategies.list() })
    },
    [DOMAIN_ROUTES.backtests]: {
      POST: async (payload) => createApiResponse(await backtesting.run(payload))
    },
    [DOMAIN_ROUTES.orders]: {
      POST: async (payload) => createApiResponse(await orders.placeOrder(payload))
    },
    [DOMAIN_ROUTES.portfolio]: {
      GET: async () => createApiResponse(portfolio.getSummary())
    },
    [DOMAIN_ROUTES.analytics]: {
      POST: async (payload) => createApiResponse(await analytics.analyze(payload))
    }
  };

  return {
    config,
    cache,
    logger,
    repositories,
    routes,
    modules: {
      analytics,
      backtesting,
      marketData,
      orders,
      portfolio,
      risk,
      strategies
    },
    async handleRequest({ route, method = "GET", payload = {} }) {
      const handler = routes[route]?.[method];
      if (!handler) {
        throw new Error(`Unsupported route: ${method} ${route}`);
      }
      return handler(payload);
    }
  };
}
