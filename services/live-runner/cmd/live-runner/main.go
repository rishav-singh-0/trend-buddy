package main

import (
	"log"

	"trend-buddy/packages/go/platform/httpx"
	"trend-buddy/services/live-runner/internal/app"
	"trend-buddy/services/live-runner/internal/config"
	transporthttp "trend-buddy/services/live-runner/internal/transport/http"
)

func main() {
	cfg := config.Load()
	service := app.New(cfg.ServiceName)
	handler := transporthttp.NewHandler(service)
	server := httpx.NewServer(cfg.Port, handler.RegisterRoutes())

	if err := httpx.ListenAndServe(server); err != nil {
		log.Fatalf("live runner service stopped with error: %v", err)
	}
}
