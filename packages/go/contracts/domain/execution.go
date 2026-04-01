package domain

import "time"

type OrderID string

type FillID string

type PositionID string

type AccountID string

type OrderSide string

type OrderType string

type OrderStatus string

type PositionDirection string

const (
	OrderSideBuy  OrderSide = "buy"
	OrderSideSell OrderSide = "sell"

	OrderTypeMarket    OrderType = "market"
	OrderTypeLimit     OrderType = "limit"
	OrderTypeStop      OrderType = "stop"
	OrderTypeStopLimit OrderType = "stop_limit"

	OrderStatusPending         OrderStatus = "pending"
	OrderStatusAccepted        OrderStatus = "accepted"
	OrderStatusPartiallyFilled OrderStatus = "partially_filled"
	OrderStatusFilled          OrderStatus = "filled"
	OrderStatusCanceled        OrderStatus = "canceled"
	OrderStatusRejected        OrderStatus = "rejected"

	PositionDirectionLong  PositionDirection = "long"
	PositionDirectionShort PositionDirection = "short"
	PositionDirectionFlat  PositionDirection = "flat"
)

type Fee struct {
	Amount   Decimal  `json:"amount"`
	Currency Currency `json:"currency"`
	Kind     string   `json:"kind,omitempty"`
}

type Order struct {
	ID             OrderID      `json:"id"`
	AccountID      AccountID    `json:"account_id,omitempty"`
	StrategyID     StrategyID   `json:"strategy_id,omitempty"`
	InstrumentID   InstrumentID `json:"instrument_id"`
	Venue          Venue        `json:"venue,omitempty"`
	Side           OrderSide    `json:"side"`
	Type           OrderType    `json:"type"`
	Status         OrderStatus  `json:"status"`
	Quantity       Decimal      `json:"quantity"`
	LimitPrice     Decimal      `json:"limit_price,omitempty"`
	StopPrice      Decimal      `json:"stop_price,omitempty"`
	FilledQuantity Decimal      `json:"filled_quantity,omitempty"`
	AverageFill    Decimal      `json:"average_fill,omitempty"`
	SubmittedAt    time.Time    `json:"submitted_at"`
	UpdatedAt      time.Time    `json:"updated_at"`
}

type Fill struct {
	ID           FillID       `json:"id"`
	OrderID      OrderID      `json:"order_id"`
	PositionID   PositionID   `json:"position_id,omitempty"`
	AccountID    AccountID    `json:"account_id,omitempty"`
	StrategyID   StrategyID   `json:"strategy_id,omitempty"`
	InstrumentID InstrumentID `json:"instrument_id"`
	Side         OrderSide    `json:"side"`
	Quantity     Decimal      `json:"quantity"`
	Price        Decimal      `json:"price"`
	Fees         []Fee        `json:"fees,omitempty"`
	ExecutedAt   time.Time    `json:"executed_at"`
}

type Position struct {
	ID            PositionID        `json:"id"`
	AccountID     AccountID         `json:"account_id,omitempty"`
	StrategyID    StrategyID        `json:"strategy_id,omitempty"`
	InstrumentID  InstrumentID      `json:"instrument_id"`
	Direction     PositionDirection `json:"direction"`
	Quantity      Decimal           `json:"quantity"`
	AverageOpen   Decimal           `json:"average_open_price,omitempty"`
	RealizedPNL   Decimal           `json:"realized_pnl,omitempty"`
	UnrealizedPNL Decimal           `json:"unrealized_pnl,omitempty"`
	OpenedAt      time.Time         `json:"opened_at"`
	ClosedAt      *time.Time        `json:"closed_at,omitempty"`
}

type Holding struct {
	InstrumentID  InstrumentID `json:"instrument_id"`
	Quantity      Decimal      `json:"quantity"`
	AveragePrice  Decimal      `json:"average_price,omitempty"`
	MarketPrice   Decimal      `json:"market_price,omitempty"`
	MarketValue   Decimal      `json:"market_value,omitempty"`
	CostBasis     Decimal      `json:"cost_basis,omitempty"`
	UnrealizedPNL Decimal      `json:"unrealized_pnl,omitempty"`
}

type PortfolioSnapshot struct {
	AccountID     AccountID `json:"account_id,omitempty"`
	Equity        Decimal   `json:"equity"`
	Cash          Decimal   `json:"cash"`
	BuyingPower   Decimal   `json:"buying_power,omitempty"`
	RealizedPNL   Decimal   `json:"realized_pnl,omitempty"`
	UnrealizedPNL Decimal   `json:"unrealized_pnl,omitempty"`
	Holdings      []Holding `json:"holdings,omitempty"`
	Timestamp     time.Time `json:"timestamp"`
}
