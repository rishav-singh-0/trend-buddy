package domain

import "time"

type LiveRunID string

type LiveRunStatus string

const (
	LiveRunStatusPending LiveRunStatus = "pending"
	LiveRunStatusRunning LiveRunStatus = "running"
	LiveRunStatusPaused  LiveRunStatus = "paused"
	LiveRunStatusStopped LiveRunStatus = "stopped"
	LiveRunStatusFailed  LiveRunStatus = "failed"
)

type LiveRun struct {
	ID           LiveRunID     `json:"id"`
	StrategyID   StrategyID    `json:"strategy_id"`
	InstrumentID InstrumentID  `json:"instrument_id"`
	Status       LiveRunStatus `json:"status"`
	StartedAt    time.Time     `json:"started_at"`
	UpdatedAt    time.Time     `json:"updated_at"`
}
