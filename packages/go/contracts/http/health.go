package httpcontracts

// HealthResponse is the common REST health payload used across services.
type HealthResponse struct {
	Service string            `json:"service"`
	Status  string            `json:"status"`
	Details map[string]string `json:"details,omitempty"`
}
