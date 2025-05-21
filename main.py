import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

API_KEY = "e8b66a8f-2d33-41e4-ad83-0557dcc3ba32"
CMC_LISTINGS_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
CMC_HISTORICAL_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/historical"

HEADERS = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": API_KEY,
}

def fetch_top_100():
    params = {"start": "1", "limit": "100", "convert": "USD"}
    response = requests.get(CMC_LISTINGS_URL, headers=HEADERS, params=params)
    data = response.json()
    return data["data"]

def fetch_historical_price(coin_id, days_ago):
    time_end = datetime.utcnow()
    time_start = time_end - timedelta(days=days_ago)
    params = {
        "id": coin_id,
        "interval": "daily",
        "time_start": time_start.isoformat(),
        "time_end": time_end.isoformat(),
        "convert": "USD"
    }
    response = requests.get(CMC_HISTORICAL_URL, headers=HEADERS, params=params)
    data = response.json()
    try:
        quotes = data["data"]["quotes"]
        return quotes[0]["quote"]["USD"]["price"] if quotes else None
    except Exception:
        return None

def main():
    st.title("CMC100 Coin Discount Tracker")

    time_frame = st.selectbox("Select Time Frame", ["1 hour", "24 hours", "3 days", "7 days", "30 days", "60 days"])
    threshold = st.selectbox("Select Discount Threshold (%)", [5, 10, 15, 20, 25, 30])

    time_frame_map = {
        "1 hour": 1/24,
        "24 hours": 1,
        "3 days": 3,
        "7 days": 7,
        "30 days": 30,
        "60 days": 60
    }
    days = time_frame_map[time_frame]

    with st.spinner("Fetching data..."):
        coins = fetch_top_100()
        discounted_coins = []

        for coin in coins:
            coin_id = coin["id"]
            name = coin["name"]
            symbol = coin["symbol"]
            current_price = coin["quote"]["USD"]["price"]
            old_price = fetch_historical_price(coin_id, days)
            if old_price:
                change_pct = ((current_price - old_price) / old_price) * 100
                if change_pct <= -threshold:
                    discounted_coins.append({
                        "Name": name,
                        "Symbol": symbol,
                        "Current Price": round(current_price, 2),
                        f"Price {int(days)}d Ago": round(old_price, 2),
                        "% Change": round(change_pct, 2)
                    })

        if discounted_coins:
            df = pd.DataFrame(discounted_coins).sort_values(by="% Change")
            st.success(f"{len(df)} coins found with ≥{threshold}% drop in last {int(days)} days.")
            st.dataframe(df)
            st.download_button("Download CSV", df.to_csv(index=False), "discounted_coins.csv", "text/csv")
        else:
            st.info("No coins found with the selected criteria.")

if __name__ == "__main__":
    main()