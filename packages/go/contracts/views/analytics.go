package views

import (
	"time"

	"trend-buddy/packages/go/contracts/domain"
)

type PerformanceSummary struct {
	Period      string         `json:"period"`
	TotalPNL    domain.Decimal `json:"total_pnl"`
	WinRate     domain.Decimal `json:"win_rate"`
	MaxDrawdown domain.Decimal `json:"max_drawdown"`
	TradeCount  int            `json:"trade_count"`
}

type PortfolioSummary struct {
	AccountID     domain.AccountID `json:"account_id,omitempty"`
	Equity        domain.Decimal   `json:"equity"`
	Cash          domain.Decimal   `json:"cash"`
	RealizedPNL   domain.Decimal   `json:"realized_pnl,omitempty"`
	UnrealizedPNL domain.Decimal   `json:"unrealized_pnl,omitempty"`
	OpenPositions int              `json:"open_positions"`
	Timestamp     time.Time        `json:"timestamp"`
}
