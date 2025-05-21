# CMC Price Drop Tracker

A Streamlit app to identify cryptocurrencies from the CMC100 Index that have dropped 10% or more over various timeframes.

## Features
- Fetch top 100 cryptocurrencies
- Select time window (1h, 24h, 3d, 7d, 30d, 60d)
- Identify coins with 10% or more price drop
- Download results as CSV

## Setup

```bash
pip install -r requirements.txt
streamlit run main.py
```

## Note

Make sure to update your CoinMarketCap API key inside `main.py`.