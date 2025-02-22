import requests
import pandas as pd
import os
import json

API_URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 100,
    "page": 1,
    "sparkline": False
}

def fetch_crypto_data():
    response = requests.get(API_URL, params=PARAMS)
    print("API Response Status Code:", response.status_code)  # Debugging line
    if response.status_code == 200:
        data = response.json()
        print("Fetched Data:", data)  # Debugging line
        return data
    else:
        print("Error fetching data:", response.status_code)
        return None

def save_to_excel(data, directory="data", filename="crypto_data.xlsx"):
    os.makedirs(directory, exist_ok=True)  # Create directory if it doesn't exist
    file_path = os.path.join(directory, filename)  # Construct full file path
    df = pd.DataFrame(data)
    df = df[['id', 'symbol', 'name', 'current_price', 'market_cap', 'total_volume', 'price_change_percentage_24h']]
    df.to_excel(file_path, index=False)  # Save as Excel file
    print(f"Data saved to {file_path}")

def upload_to_kaggle():
    dataset_metadata = {
        "title": "Daily Cryptocurrency Market Data",
        "id": "your-kaggle-username/crypto-market-daily",
        "licenses": [{"name": "CC0-1.0"}]
    }

    with open("dataset-metadata.json", "w") as f:
        json.dump(dataset_metadata, f)

    os.system("kaggle datasets version -m 'Daily update' --dir-mode zip")

if __name__ == "__main__":
    data = fetch_crypto_data()
    if data:
        save_to_excel(data)  # Call the updated function
        upload_to_kaggle()
