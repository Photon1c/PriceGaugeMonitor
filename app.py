from flask import Flask, jsonify, render_template
import os
import pandas as pd
import yfinance as yf

app = Flask(__name__)

def get_latest_prices_yfinance(symbols):
    # Fetch the latest stock prices using yfinance
    data = yf.download(tickers=symbols, period='1d', interval='1m')
    latest_prices = {symbol: data['Close'][symbol][-1] for symbol in symbols if symbol in data['Close']}
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
