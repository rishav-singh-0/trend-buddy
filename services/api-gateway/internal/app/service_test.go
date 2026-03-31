package app

import (
	"io"
	"net/http"
	"strings"
	"testing"
)

type stubHTTPClient struct {
	responses map[string]*http.Response
	errors    map[string]error
}

func (s stubHTTPClient) Do(req *http.Request) (*http.Response, error) {
	if err, ok := s.errors[req.URL.String()]; ok {
		return nil, err
	}

	if response, ok := s.responses[req.URL.String()]; ok {
		return response, nil
	}

	return &http.Response{
		StatusCode: http.StatusNotFound,
		Status:     http.StatusText(http.StatusNotFound),
		Body:       io.NopCloser(strings.NewReader(`{"service":"missing","status":"down"}`)),
	}, nil
}

func TestServiceHealthAggregatesDependencies(t *testing.T) {
	service := NewWithClient("api-gateway", stubHTTPClient{
		responses: map[string]*http.Response{
			"http://database-service:8083/health": {
				StatusCode: http.StatusOK,
				Status:     "200 OK",
				Body: io.NopCloser(strings.NewReader(
					`{"service":"database-service","status":"ok"}`,
				)),
			},
			"http://indicator-engine:8086/health": {
				StatusCode: http.StatusOK,
				Status:     "200 OK",
				Body: io.NopCloser(strings.NewReader(
					`{"service":"indicator-engine","status":"ok"}`,
				)),
			},
			"http://backtesting:8090/health": {
				StatusCode: http.StatusServiceUnavailable,
				Status:     "503 Service Unavailable",
				Body: io.NopCloser(strings.NewReader(
					`{"service":"backtesting","status":"down"}`,
				)),
			},
		},
	}, []Dependency{
		{Name: "database-service", URL: "http://database-service:8083"},
		{Name: "indicator-engine", URL: "http://indicator-engine:8086"},
		{Name: "backtesting", URL: "http://backtesting:8090"},
	})

	response := service.Health()

	if response.Service != "api-gateway" {
		t.Fatalf("expected api-gateway service name; got %q", response.Service)
	}
	if response.Status != "degraded" {
		t.Fatalf("expected degraded gateway status; got %q", response.Status)
	}
	if response.Checks["database-service"].Status != "ok" {
		t.Fatalf("expected database-service to be ok; got %q", response.Checks["database-service"].Status)
	}
	if response.Checks["database-service"].URL != "http://database-service:8083/health" {
		t.Fatalf("expected database-service URL to be propagated; got %q", response.Checks["database-service"].URL)
	}
	if response.Checks["backtesting"].Status != "down" {
		t.Fatalf("expected backtesting to be down; got %q", response.Checks["backtesting"].Status)
	}
	if response.Checks["backtesting"].URL != "http://backtesting:8090/health" {
		t.Fatalf("expected backtesting URL to be propagated; got %q", response.Checks["backtesting"].URL)
	}
}
