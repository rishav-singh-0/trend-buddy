buddy/
├── buddy/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── api/
│   ├── data/
│   │   ├── views.py
│   │   ├── models.py
│   │   └── ...
│   ├── data_processing/
│   │   ├── views.py
│   │   ├── models.py
│   │   └── ...
│   └── ...
│
├── analysis/
│   ├── backtesting/
│   │   ├── views.py
│   │   ├── models.py
│   │   └── ...
│   ├── recommendations/
│   │   ├── views.py
│   │   ├── models.py
│   │   └── ...
│   └── ...
│
├── frontend/
│   ├── static/
│   ├── templates/
│   ├── views.py
│   └── ...
│
└── manage.py


# API

## Data

Database Structure for Stock Analysis Web App

### Exchange
- Represents different stock exchanges
- Holds information about exchange names

### Symbol
- Represents individual stocks or securities
- Linked to the respective exchange through a ForeignKey

### Candle
- Represents historical candlestick data for stocks
- Captures open, high, low, close prices, volume, and trade counts
- Associated with a specific symbol and timestamp (time interval)

## TODO

### Favourite
- Represents a user's favorite stock symbols
- Captures the user and the symbol they've favorited
- Provides a mechanism for users to track and manage their favorite stocks

### FundamentalData
- Represents fundamental data for stocks.
- Linked to the Symbol model to associate data with specific stocks.
- Fields can store information like earnings, revenue, ratios, etc.

### TechnicalData
- Represents technical data for stocks.
- Linked to the Symbol model to associate data with specific stocks.
- Fields can store information about moving averages, RSI, MACD, etc.
