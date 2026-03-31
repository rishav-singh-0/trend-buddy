package health

import httpcontracts "trend-buddy/packages/go/contracts/http"

// OK returns the common service health shape.
func OK(service string, details map[string]string) httpcontracts.HealthResponse {
	return httpcontracts.HealthResponse{
		Service: service,
		Status:  "ok",
		Details: details,
	}
}
