package httpcontracts

type DependencyHealth struct {
	Status string `json:"status"`
	URL    string `json:"url,omitempty"`
}

// HealthResponse is the common REST health payload used across services.
type HealthResponse struct {
	Service string                      `json:"service"`
	Status  string                      `json:"status"`
	Checks  map[string]DependencyHealth `json:"checks,omitempty"`
}
