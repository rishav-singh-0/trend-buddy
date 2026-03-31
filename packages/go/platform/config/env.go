package config

import (
	"os"
	"strconv"
)

// String returns the env value or the fallback when it is unset.
func String(key, fallback string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}

	return fallback
}

// Int returns the env value parsed as int or the fallback when it is unset or invalid.
func Int(key string, fallback int) int {
	if value := os.Getenv(key); value != "" {
		if parsed, err := strconv.Atoi(value); err == nil {
			return parsed
		}
	}

	return fallback
}
