package domain

import "time"

type CandleKey struct {
	InstrumentID InstrumentID `json:"instrument_id"`
	Timeframe    Timeframe    `json:"timeframe"`
}

type Candle struct {
	InstrumentID InstrumentID `json:"instrument_id"`
	Timeframe    Timeframe    `json:"timeframe"`
	Timestamp    time.Time    `json:"timestamp"`
	Open         Decimal      `json:"open"`
	High         Decimal      `json:"high"`
	Low          Decimal      `json:"low"`
	Close        Decimal      `json:"close"`
	Volume       Decimal      `json:"volume"`
}

type Quote struct {
	InstrumentID InstrumentID `json:"instrument_id"`
	Timestamp    time.Time    `json:"timestamp"`
	BidPrice     Decimal      `json:"bid_price"`
	AskPrice     Decimal      `json:"ask_price"`
	BidSize      Decimal      `json:"bid_size,omitempty"`
	AskSize      Decimal      `json:"ask_size,omitempty"`
}
