package app

import (
	"encoding/json"
	"net/http"
	"strings"
	"time"

	httpcontracts "trend-buddy/packages/go/contracts/http"
	"trend-buddy/packages/go/platform/health"
)

type HTTPClient interface {
	Do(req *http.Request) (*http.Response, error)
}

type Dependency struct {
	Name string
	URL  string
}

type Service struct {
	name         string
	client       HTTPClient
	dependencies []Dependency
}

func New(name string, dependencies []Dependency) *Service {
	return NewWithClient(name, &http.Client{Timeout: 2 * time.Second}, dependencies)
}

func NewWithClient(name string, client HTTPClient, dependencies []Dependency) *Service {
	normalizedDependencies := make([]Dependency, 0, len(dependencies))
	for _, dependency := range dependencies {
		normalizedDependencies = append(normalizedDependencies, Dependency{
			Name: dependency.Name,
			URL:  strings.TrimRight(dependency.URL, "/"),
		})
	}

	return &Service{
		name:         name,
		client:       client,
		dependencies: normalizedDependencies,
	}
}

func (s *Service) Health() httpcontracts.HealthResponse {
	checks := make(map[string]httpcontracts.DependencyHealth, len(s.dependencies))
	status := "ok"

	for _, dependency := range s.dependencies {
		check := s.checkDependency(dependency)
		checks[dependency.Name] = check
		if check.Status != "ok" {
			status = "degraded"
		}
	}

	response := health.OK(s.name)
	response.Status = status
	response.Checks = checks

	return response
}

func (s *Service) checkDependency(dependency Dependency) httpcontracts.DependencyHealth {
	healthURL := dependency.URL + "/health"
	request, err := http.NewRequest(http.MethodGet, healthURL, nil)
	if err != nil {
		return httpcontracts.DependencyHealth{
			Status: "down",
			URL:    healthURL,
		}
	}

	response, err := s.client.Do(request)
	if err != nil {
		return httpcontracts.DependencyHealth{
			Status: "down",
			URL:    healthURL,
		}
	}
	defer response.Body.Close()

	var payload httpcontracts.HealthResponse
	if err := json.NewDecoder(response.Body).Decode(&payload); err != nil {
		return httpcontracts.DependencyHealth{
			Status: "down",
			URL:    healthURL,
		}
	}

	check := httpcontracts.DependencyHealth{
		Status: payload.Status,
		URL:    healthURL,
	}
	if response.StatusCode >= http.StatusBadRequest {
		check.Status = "down"
	}
	if check.Status == "" {
		check.Status = "down"
	}

	return check
}
