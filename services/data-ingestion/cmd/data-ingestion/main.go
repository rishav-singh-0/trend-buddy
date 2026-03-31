package main

import (
	"log"

	"trend-buddy/packages/go/platform/httpx"
	"trend-buddy/services/data-ingestion/internal/app"
	"trend-buddy/services/data-ingestion/internal/config"
	transporthttp "trend-buddy/services/data-ingestion/internal/transport/http"
)

func main() {
	cfg := config.Load()
	service := app.New(cfg.ServiceName)
	handler := transporthttp.NewHandler(service)
	server := httpx.NewServer(cfg.Port, handler.RegisterRoutes())

	if err := httpx.ListenAndServe(server); err != nil {
		log.Fatalf("data ingestion service stopped with error: %v", err)
	}
}
