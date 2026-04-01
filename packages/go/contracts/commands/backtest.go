package commands

import (
	"time"

	"trend-buddy/packages/go/contracts/domain"
)

type BacktestRequest struct {
	StrategyID     domain.StrategyID   `json:"strategy_id"`
	InstrumentID   domain.InstrumentID `json:"instrument_id"`
	Timeframe      domain.Timeframe    `json:"timeframe"`
	StartTime      time.Time           `json:"start_time"`
	EndTime        time.Time           `json:"end_time"`
	InitialCapital domain.Decimal      `json:"initial_capital"`
	Fees           domain.Decimal      `json:"fees,omitempty"`
	Slippage       domain.Decimal      `json:"slippage,omitempty"`
	Parameters     map[string]any      `json:"parameters,omitempty"`
}
