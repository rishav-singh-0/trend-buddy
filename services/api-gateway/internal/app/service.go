package app

import (
	httpcontracts "trend-buddy/packages/go/contracts/http"
	"trend-buddy/packages/go/platform/health"
)

type Service struct {
	name string
}

func New(name string) *Service {
	return &Service{name: name}
}

func (s *Service) Health() httpcontracts.HealthResponse {
	return health.OK(s.name, map[string]string{
		"entrypoint": "gateway",
	})
}
