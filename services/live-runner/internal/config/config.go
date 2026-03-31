package config

import platformconfig "trend-buddy/packages/go/platform/config"

type Config struct {
	Port        int
	ServiceName string
}

func Load() Config {
	return Config{
		Port:        platformconfig.Int("LIVE_RUNNER_PORT", 8087),
		ServiceName: "live-runner",
	}
}
