package main

import (
	"log"

	"trend-buddy/packages/go/platform/httpx"
	"trend-buddy/services/api-gateway/internal/app"
	"trend-buddy/services/api-gateway/internal/config"
	transporthttp "trend-buddy/services/api-gateway/internal/transport/http"
)

func main() {
	cfg := config.Load()
	service := app.New(cfg.ServiceName, []app.Dependency{
		{Name: "database-service", URL: cfg.DatabaseServiceURL},
		{Name: "data-ingestion", URL: cfg.DataIngestionURL},
		{Name: "broker-gateway", URL: cfg.BrokerGatewayURL},
		{Name: "indicator-engine", URL: cfg.IndicatorEngineURL},
		{Name: "live-runner", URL: cfg.LiveRunnerURL},
		{Name: "backtesting", URL: cfg.BacktestingServiceURL},
		{Name: "strategy-engine", URL: cfg.StrategyEngineURL},
		{Name: "portfolio-analytics", URL: cfg.PortfolioAnalyticsURL},
	})
	handler := transporthttp.NewHandler(service)
	server := httpx.NewServer(cfg.Port, handler.RegisterRoutes())

	if err := httpx.ListenAndServe(server); err != nil {
		log.Fatalf("api gateway stopped with error: %v", err)
	}
}
