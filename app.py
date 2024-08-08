from flask import Flask, jsonify, render_template
import os
import pandas as pd
import yfinance as yf
from dotenv import load_dotenv
import numpy as np

app = Flask(__name__)
load_dotenv()

def get_latest_prices_yfinance(symbols):
    data = yf.download(tickers=symbols, period='1d', interval='1m')
    latest_prices = {}
    for symbol in symbols:
        try:
            latest_price = data['Close'][symbol][-1]
            # Replace NaN values with None
            latest_prices[symbol] = None if np.isnan(latest_price) else latest_price
        except KeyError:
            latest_prices[symbol] = None
    return latest_prices

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prices', methods=['GET'])
def prices():
    file = pd.read_csv("F:\inputs\option_holdings.csv")
    symbol_list = file['symbol'].dropna().tolist()
    latest_prices = get_latest_prices_yfinance(symbol_list)
    return jsonify(latest_prices)

if __name__ == '__main__':
    app.run(debug=True)
