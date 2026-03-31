package config

import platformconfig "trend-buddy/packages/go/platform/config"

type Config struct {
	Port        int
	ServiceName string
}

func Load() Config {
	return Config{
		Port:        platformconfig.Int("API_GATEWAY_PORT", platformconfig.Int("PORT", 8080)),
		ServiceName: "api-gateway",
	}
}
