package main

import (
	"log"

	"trend-buddy/packages/go/platform/httpx"
	"trend-buddy/services/database-service/internal/adapters/sqlite"
	"trend-buddy/services/database-service/internal/app"
	"trend-buddy/services/database-service/internal/config"
	transporthttp "trend-buddy/services/database-service/internal/transport/http"
)

func main() {
	cfg := config.Load()
	db := sqlite.New(cfg.DatabaseURL)
	service := app.New(cfg.ServiceName, db)
	handler := transporthttp.NewHandler(service)
	server := httpx.NewServer(cfg.Port, handler.RegisterRoutes())

	if err := httpx.ListenAndServe(server); err != nil {
		log.Fatalf("database service stopped with error: %v", err)
	}
}
