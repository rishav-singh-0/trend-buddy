package commands

import (
	"time"

	"trend-buddy/packages/go/contracts/domain"
)

type IndicatorRequest struct {
	Indicator    string              `json:"indicator"`
	InstrumentID domain.InstrumentID `json:"instrument_id"`
	Timeframe    domain.Timeframe    `json:"timeframe"`
	StartTime    time.Time           `json:"start_time"`
	EndTime      time.Time           `json:"end_time"`
	Parameters   map[string]any      `json:"parameters,omitempty"`
}
