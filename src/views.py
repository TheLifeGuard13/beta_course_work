import datetime
import logging
import os
from pathlib import Path

import requests
import yfinance as yf
from dotenv import load_dotenv

data_path_log = Path(__file__).parent.parent.joinpath("data", "views.log")
logger = logging.getLogger("__views__")
file_handler = logging.FileHandler(data_path_log, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def get_stock_prices(stocks: list, date_obj: datetime.datetime) -> list[dict]:
    """выгружает через модуль yfinance курсы выбранных акций в выбранную дату
    и выдает в форме списка словарей"""
    try:
        start_date = date_obj.strftime("%Y-%m-%d")
        end_date = (date_obj + datetime.timedelta(days=3)).strftime("%Y-%m-%d")
        stock_list = []
        for stock in stocks:
            dict_ = {}
            stock_data = yf.Ticker(stock)
            data = stock_data.history(start=start_date, end=end_date).head(1)
            one_date_data = data.to_dict(orient="records")[0]
            stock_price = round(one_date_data["Close"], 2)
            dict_[stock] = stock_price
            stock_list.append(dict_)
        logger.info("Котировки успешно получены")
        return stock_list
    except Exception as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции get_stock_prices()")
        raise error


def get_currency_rates(currencies: list, date_obj: datetime.datetime) -> list[dict]:
    """выгружает через APILAYER выбранные курсы валют в выбранную дату
    и выдает в форме списка словарей"""
    load_dotenv()
    start_date = date_obj.strftime("%Y-%m-%d")
    end_date = date_obj.strftime("%Y-%m-%d")
    url = (f"https://api.apilayer.com/exchangerates_data/timeseries?"
           f"start_date={start_date}&end_date={end_date}&base=RUB")
    api_key = os.getenv("APILAYER_KEY")
    headers = {"apikey": api_key}
    try:
        response = requests.get(url, headers=headers, data=[])
        currency_dict = response.json()
        currency_list = []
        for currency in currencies:
            dict_ = {}
            dict_["currency"] = currency
            dict_["rate"] = round(1 / float(currency_dict["rates"][start_date][currency]), 2)
            currency_list.append(dict_)
        logger.info("Курсы валют успешно получены")
        return currency_list
    except Exception as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции get_exchange_rate()")
        raise error
