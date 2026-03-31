package app

import (
	httpcontracts "trend-buddy/packages/go/contracts/http"
	"trend-buddy/services/database-service/internal/ports"
)

type Service struct {
	name string
	db   ports.HealthReporter
}

func New(name string, db ports.HealthReporter) *Service {
	return &Service{name: name, db: db}
}

func (s *Service) Health() httpcontracts.HealthResponse {
	details := s.db.Health()
	status := "ok"
	if details["status"] == "down" {
		status = "down"
	}

	return httpcontracts.HealthResponse{
		Service: s.name,
		Status:  status,
		Details: details,
	}
}
