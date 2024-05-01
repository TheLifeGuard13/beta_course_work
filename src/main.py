from pprint import pprint

from config import OPERATIONS_PATH, STOCKS_CURRENCIES_PATH
from src.utils import (
    get_cards_payments,
    get_converted_date,
    get_greeting_phrase,
    filter_operations_by_date,
    load_json_file,
    load_xlsx_file,
    get_top_five_operations,
)
from src.views import get_currency_rates, get_stock_prices

if __name__ == "__main__":
    input_date = "2021-12-13 16:00:00"

    user_stocks = load_json_file(STOCKS_CURRENCIES_PATH)["user_stocks"]
    user_currencies = load_json_file(STOCKS_CURRENCIES_PATH)["user_currencies"]

    def main_page(date: str) -> dict:
        """принимает на вход строку с датой, возвращает json-ответ с данными для главной страницы"""
        date_obj = get_converted_date(date)
        filtered_operations_by_date = filter_operations_by_date(load_xlsx_file(OPERATIONS_PATH), date_obj)
        dict_ = dict()
        dict_["greeting"] = get_greeting_phrase()
        dict_["cards"] = get_cards_payments(filtered_operations_by_date)
        dict_["top_transactions"] = get_top_five_operations(filtered_operations_by_date)
        dict_["currency_rates"] = get_currency_rates(user_currencies, date_obj)
        dict_["stock_prices"] = get_stock_prices(user_stocks, date_obj)
        return dict_

    pprint(main_page(input_date))
