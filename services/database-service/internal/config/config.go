package config

import platformconfig "trend-buddy/packages/go/platform/config"

type Config struct {
	Port        int
	ServiceName string
	DatabaseURL string
}

func Load() Config {
	return Config{
		Port:        platformconfig.Int("DATABASE_SERVICE_PORT", 8083),
		ServiceName: "database-service",
		DatabaseURL: platformconfig.String("DB_URL", "file:/app/db/trend-buddy.db?cache=shared&_foreign_keys=on"),
	}
}
