import datetime
import json
import os
import logging
from pathlib import Path

import requests
import yfinance as yf
from dotenv import load_dotenv

data_path_log = Path(__file__).parent.parent.joinpath("data", "views.log")
logger = logging.getLogger("__views__")

if os.path.exists(data_path_log):
    os.remove(data_path_log)

file_handler = logging.FileHandler(data_path_log, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def get_stock_prices(stocks: list, date_obj: datetime) -> list[dict]:
    """
    получает курсы выбранных акций в выбранную дату через модуль yfinance
    и выдает в форме списка словарей
    param: список акций
    param: дата в формате date_obj
    return: список котировок акций
    """
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
        logger.error(f'Произошла ошибка: {str(error)} в функции get_stock_prices()')
        raise error


def get_exchange_rate(currencies: list, date_obj: datetime) -> list[dict]:
    """
    получает курсы валют в выбранную дату через APILAYER API
    и выдает в форме списка словарей
    param: список акций
    param: дата в формате date_obj
    return: список курсов валют
    """
    load_dotenv()
    start_date = date_obj.strftime("%Y-%m-%d")
    end_date = date_obj.strftime("%Y-%m-%d")
    url = (
        f"https://api.apilayer.com/exchangerates_data/timeseries?start_date={start_date}&end_date={end_date}&base=RUB"
    )
    try:
        api_key = os.getenv("APILAYER_KEY")
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
        logger.info("Курсы валют успешно получены")
        return currency_list
    except Exception as error:
        logger.error(f'Произошла ошибка: {str(error)} в функции get_exchange_rate()')
        raise error
