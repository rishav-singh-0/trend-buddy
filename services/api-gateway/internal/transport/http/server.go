package transporthttp

import httpcontracts "trend-buddy/packages/go/contracts/http"

type Service interface {
	Health() httpcontracts.HealthResponse
}

type Handler struct {
	service Service
}

func NewHandler(service Service) *Handler {
	return &Handler{service: service}
}
