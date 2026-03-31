package transporthttp

import (
	"net/http"
	"net/http/httptest"
	"testing"

	httpcontracts "trend-buddy/packages/go/contracts/http"
)

type stubService struct{}

func (stubService) Health() httpcontracts.HealthResponse {
	return httpcontracts.HealthResponse{Service: "database-service", Status: "ok"}
}

func TestHealthHandler(t *testing.T) {
	handler := NewHandler(stubService{})
	req, err := http.NewRequest(http.MethodGet, "/health", nil)
	if err != nil {
		t.Fatalf("request failed: %v", err)
	}
	resp := httptest.NewRecorder()
	handler.RegisterRoutes().ServeHTTP(resp, req)

	if resp.Code != http.StatusOK {
		t.Fatalf("expected status 200, got %d", resp.Code)
	}
}
