package config

import platformconfig "trend-buddy/packages/go/platform/config"

type Config struct {
	Port                  int
	ServiceName           string
	DatabaseServiceURL    string
	DataIngestionURL      string
	BrokerGatewayURL      string
	IndicatorEngineURL    string
	LiveRunnerURL         string
	BacktestingServiceURL string
	StrategyEngineURL     string
	PortfolioAnalyticsURL string
}

func Load() Config {
	return Config{
		Port:                  platformconfig.Int("API_GATEWAY_PORT", platformconfig.Int("PORT", 8080)),
		ServiceName:           "api-gateway",
		DatabaseServiceURL:    platformconfig.ServiceURL("DATABASE_SERVICE_URL", "database-service", 8083),
		DataIngestionURL:      platformconfig.ServiceURL("DATA_INGESTION_URL", "data-ingestion", 8084),
		BrokerGatewayURL:      platformconfig.ServiceURL("BROKER_GATEWAY_URL", "broker-gateway", 8085),
		IndicatorEngineURL:    platformconfig.ServiceURL("INDICATOR_ENGINE_URL", "indicator-engine", 8086),
		LiveRunnerURL:         platformconfig.ServiceURL("LIVE_RUNNER_URL", "live-runner", 8087),
		BacktestingServiceURL: platformconfig.ServiceURL("BACKTESTING_URL", "backtesting", 8090),
		StrategyEngineURL:     platformconfig.ServiceURL("STRATEGY_ENGINE_URL", "strategy-engine", 8091),
		PortfolioAnalyticsURL: platformconfig.ServiceURL("PORTFOLIO_ANALYTICS_URL", "portfolio-analytics", 8092),
	}
}
