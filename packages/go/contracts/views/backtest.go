package views

import (
	"time"

	"trend-buddy/packages/go/contracts/domain"
)

type IndicatorPoint struct {
	Timestamp time.Time      `json:"timestamp"`
	Value     domain.Decimal `json:"value"`
}

type IndicatorSeries struct {
	Indicator string           `json:"indicator"`
	Values    []IndicatorPoint `json:"values,omitempty"`
}

type EquityPoint struct {
	Timestamp time.Time      `json:"timestamp"`
	Equity    domain.Decimal `json:"equity"`
}

type BacktestResult struct {
	RunID       string             `json:"run_id"`
	StrategyID  domain.StrategyID  `json:"strategy_id"`
	Summary     PerformanceSummary `json:"summary"`
	Fills       []domain.Fill      `json:"fills,omitempty"`
	EquityCurve []EquityPoint      `json:"equity_curve,omitempty"`
}
