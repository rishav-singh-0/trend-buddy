package app

import httpcontracts "trend-buddy/packages/go/contracts/http"

type Service struct {
	name string
}

func New(name string) *Service {
	return &Service{name: name}
}

func (s *Service) Health() httpcontracts.HealthResponse {
	return httpcontracts.HealthResponse{
		Service: s.name,
		Status:  "ok",
		Details: map[string]string{"role": "indicator-computation"},
	}
}
