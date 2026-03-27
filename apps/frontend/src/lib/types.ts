export type EquityPoint = {
	session: string;
	close: number;
};

export type PortfolioHolding = {
	symbol: string;
	sector: string;
	allocation_pct: number;
	pnl_pct: number;
};

export type PortfolioSummary = {
	total_value: number;
	daily_pnl: number;
	total_pnl: number;
	cash_balance: number;
	top_sector: string;
	equity_curve: EquityPoint[];
	holdings: PortfolioHolding[];
};

export type MarketSnapshot = {
	symbol: string;
	price: number;
	change_pct: number;
	signal: string;
	generated_at: string;
};
