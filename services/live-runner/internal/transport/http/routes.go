package transporthttp

import (
	"net/http"

	httpcontracts "trend-buddy/packages/go/contracts/http"
	"trend-buddy/packages/go/platform/httpx"
)

type Service interface {
	Health() httpcontracts.HealthResponse
}

type Handler struct {
	service Service
}

func NewHandler(service Service) *Handler {
	return &Handler{service: service}
}

func (h *Handler) RegisterRoutes() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("/health", h.healthHandler)
	return mux
}

func (h *Handler) healthHandler(w http.ResponseWriter, r *http.Request) {
	httpx.WriteJSON(w, http.StatusOK, h.service.Health())
}
