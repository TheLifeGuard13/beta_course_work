from pprint import pprint

from config import OPERATIONS_PATH, STOCKS_CURRENCIES_PATH
from src.utils import (get_cards_info, get_converted_date, get_greeting_phrase, get_modified_df, load_json_file,
                       load_xlsx_file, top_five_transactions)
from src.views import get_exchange_rate, get_stock_prices

if __name__ == "__main__":
    input_date = "2021-10-16 16:00:00"

    user_stocks = load_json_file(STOCKS_CURRENCIES_PATH)["user_stocks"]
    user_currencies = load_json_file(STOCKS_CURRENCIES_PATH)["user_currencies"]

    def main_page(date: str) -> dict:
        date_obj = get_converted_date(date)
        selected_df = get_modified_df(load_xlsx_file(OPERATIONS_PATH), date_obj)
        dict_ = {}
        dict_["greeting"] = get_greeting_phrase()
        dict_["cards"] = get_cards_info(selected_df)
        dict_["top_transactions"] = top_five_transactions(selected_df)
        # dict_["currency_rates"] = get_exchange_rate(user_currencies, date_obj)
        # dict_["stock_prices"] = get_stock_prices(user_stocks, date_obj)
        return dict_

    pprint(main_page(input_date))
