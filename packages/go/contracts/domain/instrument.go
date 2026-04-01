package domain

type InstrumentID string

type Venue string

type AssetClass string

type Timeframe string

const (
	AssetClassEquity AssetClass = "equity"
	AssetClassOption AssetClass = "option"
	AssetClassFuture AssetClass = "future"
	AssetClassForex  AssetClass = "forex"
	AssetClassCrypto AssetClass = "crypto"
)

type Instrument struct {
	ID            InstrumentID `json:"id"`
	Symbol        string       `json:"symbol"`
	Venue         Venue        `json:"venue,omitempty"`
	AssetClass    AssetClass   `json:"asset_class"`
	BaseCurrency  Currency     `json:"base_currency,omitempty"`
	QuoteCurrency Currency     `json:"quote_currency,omitempty"`
	TickSize      Decimal      `json:"tick_size,omitempty"`
	LotSize       Decimal      `json:"lot_size,omitempty"`
}
