package config

import "testing"

func TestServiceURLUsesComposeDefault(t *testing.T) {
	t.Setenv("DATABASE_SERVICE_URL", "")

	got := ServiceURL("DATABASE_SERVICE_URL", "database-service", 8083)

	if got != "http://database-service:8083" {
		t.Fatalf("expected compose default URL, got %q", got)
	}
}

func TestServiceURLUsesExplicitEnv(t *testing.T) {
	t.Setenv("DATABASE_SERVICE_URL", "http://db.internal:9000")

	got := ServiceURL("DATABASE_SERVICE_URL", "database-service", 8083)

	if got != "http://db.internal:9000" {
		t.Fatalf("expected explicit env URL, got %q", got)
	}
}
