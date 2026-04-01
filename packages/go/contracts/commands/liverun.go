package commands

import "trend-buddy/packages/go/contracts/domain"

type LiveRunControlAction string

const (
	LiveRunControlStart LiveRunControlAction = "start"
	LiveRunControlPause LiveRunControlAction = "pause"
	LiveRunControlStop  LiveRunControlAction = "stop"
)

type LiveRunControlRequest struct {
	RunID        domain.LiveRunID     `json:"run_id,omitempty"`
	StrategyID   domain.StrategyID    `json:"strategy_id"`
	InstrumentID domain.InstrumentID  `json:"instrument_id"`
	Action       LiveRunControlAction `json:"action"`
	Parameters   map[string]any       `json:"parameters,omitempty"`
}
