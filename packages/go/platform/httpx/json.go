package httpx

import (
	"encoding/json"
	"net/http"
)

// WriteJSON writes a JSON response with the given HTTP status.
func WriteJSON(w http.ResponseWriter, status int, payload any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(payload)
}
