package ports

type HealthReporter interface {
	Health() map[string]string
	Close() error
}
