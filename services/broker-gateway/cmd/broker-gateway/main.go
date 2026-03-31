package main

import (
	"log"

	"trend-buddy/packages/go/platform/httpx"
	"trend-buddy/services/broker-gateway/internal/app"
	"trend-buddy/services/broker-gateway/internal/config"
	transporthttp "trend-buddy/services/broker-gateway/internal/transport/http"
)

func main() {
	cfg := config.Load()
	service := app.New(cfg.ServiceName)
	handler := transporthttp.NewHandler(service)
	server := httpx.NewServer(cfg.Port, handler.RegisterRoutes())

	if err := httpx.ListenAndServe(server); err != nil {
		log.Fatalf("broker gateway service stopped with error: %v", err)
	}
}
