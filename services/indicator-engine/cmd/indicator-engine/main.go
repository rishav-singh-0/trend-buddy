package main

import (
	"log"

	"trend-buddy/packages/go/platform/httpx"
	"trend-buddy/services/indicator-engine/internal/app"
	"trend-buddy/services/indicator-engine/internal/config"
	transporthttp "trend-buddy/services/indicator-engine/internal/transport/http"
)

func main() {
	cfg := config.Load()
	service := app.New(cfg.ServiceName)
	handler := transporthttp.NewHandler(service)
	server := httpx.NewServer(cfg.Port, handler.RegisterRoutes())

	if err := httpx.ListenAndServe(server); err != nil {
		log.Fatalf("indicator engine service stopped with error: %v", err)
	}
}
