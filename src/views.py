import json
import yfinance as yf
import datetime
from dotenv import load_dotenv
import os
import requests


def get_stock_prices(stocks: list, date_obj: datetime) -> list[dict]:
    """функция"""
    start_date = date_obj.strftime("%Y-%m-%d")
    end_date = (date_obj + datetime.timedelta(days=3)).strftime("%Y-%m-%d")
    stock_list = []
    for stock in stocks:
        dict_ = {}
        stock_data = yf.Ticker(stock)
        data = stock_data.history(start=start_date, end=end_date).head(1)
        one_date_data = data.to_dict(orient="records")[0]
        stock_price = round(one_date_data['Close'], 2)
        dict_[stock] = stock_price
        stock_list.append(dict_)
    return stock_list


def get_exchange_rate(currencies: list, date_obj: datetime) -> list[dict]:
    """"функция"""
    load_dotenv()
    api_key = os.getenv('APILAYER_KEY')
    start_date = date_obj.strftime("%Y-%m-%d")
    end_date = date_obj.strftime("%Y-%m-%d")
    url = f'https://api.apilayer.com/exchangerates_data/timeseries?start_date={start_date}&end_date={end_date}&base=RUB'
    headers = {"apikey": api_key}
    payload = []
    response = requests.request("GET", url, headers=headers, data=payload)
    currency_dict = json.loads(response.text)
    currency_list = []
    for currency in currencies:
        dict_ = {}
        dict_["currency"] = currency
        dict_["rate"] = round(1 / currency_dict["rates"][start_date][currency], 2)
        currency_list.append(dict_)
    return currency_list
