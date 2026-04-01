package config

import (
	"fmt"
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

// Bool returns the env value parsed as bool or the fallback when it is unset or invalid.
func Bool(key string, fallback bool) bool {
	if value := os.Getenv(key); value != "" {
		if parsed, err := strconv.ParseBool(value); err == nil {
			return parsed
		}
	}

	return fallback
}

// ServiceURL returns the configured service URL or a default Docker Compose service URL.
func ServiceURL(key, serviceName string, port int) string {
	return String(key, fmt.Sprintf("http://%s:%d", serviceName, port))
}
