package config

import platformconfig "trend-buddy/packages/go/platform/config"

type Config struct {
	Port                  int
	ServiceName           string
	DatabaseServiceURL    string
	IndicatorEngineURL    string
	BacktestingServiceURL string
}

func Load() Config {
	return Config{
		Port:                  platformconfig.Int("API_GATEWAY_PORT", platformconfig.Int("PORT", 8080)),
		ServiceName:           "api-gateway",
		DatabaseServiceURL:    platformconfig.String("DATABASE_SERVICE_URL", "http://database-service:8083"),
		IndicatorEngineURL:    platformconfig.String("INDICATOR_ENGINE_URL", "http://indicator-engine:8086"),
		BacktestingServiceURL: platformconfig.String("BACKTESTING_SERVICE_URL", "http://backtesting:8090"),
	}
}
