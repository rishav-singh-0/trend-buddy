package app

import (
	httpcontracts "trend-buddy/packages/go/contracts/http"
	"trend-buddy/packages/go/platform/health"
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
	}
}

func (s *Service) Ready() httpcontracts.HealthResponse {
	return health.OK(s.name)
}
