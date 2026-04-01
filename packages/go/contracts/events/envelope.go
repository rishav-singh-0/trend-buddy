package events

import "time"

// Envelope is the shared async event wrapper across services.
type Envelope struct {
	Type      string    `json:"type"`
	Source    string    `json:"source"`
	Subject   string    `json:"subject,omitempty"`
	Timestamp time.Time `json:"timestamp"`
	Data      any       `json:"data,omitempty"`
}

// StreamEnvelope is the shared streaming wrapper for websocket and live feeds.
type StreamEnvelope struct {
	Topic     string    `json:"topic"`
	Type      string    `json:"type"`
	Timestamp time.Time `json:"timestamp"`
	Data      any       `json:"data,omitempty"`
}
