package transporthttp

import (
	"net/http"

	"trend-buddy/packages/go/platform/httpx"
)

func (h *Handler) RegisterRoutes() http.Handler {
	mux := http.NewServeMux()

	mux.HandleFunc("/", h.helloWorldHandler)
	mux.HandleFunc("/api/v1/health", h.healthHandler)
	mux.HandleFunc("/health", h.healthHandler)
	mux.HandleFunc("/api/v1/ready", h.readyHandler)
	mux.HandleFunc("/ready", h.readyHandler)

	return h.corsMiddleware(mux)
}

func (h *Handler) corsMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS, PATCH")
		w.Header().Set("Access-Control-Allow-Headers", "Accept, Authorization, Content-Type, X-CSRF-Token")
		w.Header().Set("Access-Control-Allow-Credentials", "false")

		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusNoContent)
			return
		}

		next.ServeHTTP(w, r)
	})
}

func (h *Handler) helloWorldHandler(w http.ResponseWriter, r *http.Request) {
	httpx.WriteJSON(w, http.StatusOK, map[string]string{"message": "Hello World"})
}

func (h *Handler) healthHandler(w http.ResponseWriter, r *http.Request) {
	httpx.WriteJSON(w, http.StatusOK, h.service.Health())
}

func (h *Handler) readyHandler(w http.ResponseWriter, r *http.Request) {
	httpx.WriteJSON(w, http.StatusOK, h.service.Ready())
}
