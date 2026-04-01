package domain

import "time"

type StrategyID string

type StrategyState string

type SignalAction string

const (
	StrategyStateDraft    StrategyState = "draft"
	StrategyStateActive   StrategyState = "active"
	StrategyStateArchived StrategyState = "archived"

	SignalActionEnterLong  SignalAction = "enter_long"
	SignalActionExitLong   SignalAction = "exit_long"
	SignalActionEnterShort SignalAction = "enter_short"
	SignalActionExitShort  SignalAction = "exit_short"
	SignalActionHold       SignalAction = "hold"
)

type StrategyDefinition struct {
	ID            StrategyID     `json:"id"`
	Name          string         `json:"name"`
	Version       string         `json:"version"`
	State         StrategyState  `json:"state"`
	InstrumentIDs []InstrumentID `json:"instrument_ids,omitempty"`
	IndicatorRefs []string       `json:"indicator_refs,omitempty"`
	Parameters    map[string]any `json:"parameters,omitempty"`
}

type StrategySignal struct {
	StrategyID   StrategyID     `json:"strategy_id"`
	InstrumentID InstrumentID   `json:"instrument_id"`
	Action       SignalAction   `json:"action"`
	Timestamp    time.Time      `json:"timestamp"`
	Strength     Decimal        `json:"strength,omitempty"`
	Metadata     map[string]any `json:"metadata,omitempty"`
}
