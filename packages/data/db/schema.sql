CREATE TABLE market_candles (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  provider VARCHAR(32) NOT NULL,
  symbol VARCHAR(32) NOT NULL,
  interval_code VARCHAR(8) NOT NULL,
  open_price DECIMAL(18, 4) NOT NULL,
  high_price DECIMAL(18, 4) NOT NULL,
  low_price DECIMAL(18, 4) NOT NULL,
  close_price DECIMAL(18, 4) NOT NULL,
  volume BIGINT NOT NULL,
  candle_time DATETIME NOT NULL
);

CREATE TABLE order_events (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  broker VARCHAR(32) NOT NULL,
  symbol VARCHAR(32) NOT NULL,
  side VARCHAR(8) NOT NULL,
  quantity DECIMAL(18, 4) NOT NULL,
  price DECIMAL(18, 4) NOT NULL,
  status VARCHAR(16) NOT NULL,
  placed_at DATETIME NOT NULL
);

CREATE TABLE backtest_runs (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  strategy_code VARCHAR(64) NOT NULL,
  symbol VARCHAR(32) NOT NULL,
  interval_code VARCHAR(8) NOT NULL,
  net_pnl DECIMAL(18, 4) NOT NULL,
  max_drawdown DECIMAL(18, 4) NOT NULL,
  created_at DATETIME NOT NULL
);

CREATE TABLE analytics_reports (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  symbol VARCHAR(32) NOT NULL,
  report_type VARCHAR(32) NOT NULL,
  advisory_score DECIMAL(5, 2) NOT NULL,
  created_at DATETIME NOT NULL
);
