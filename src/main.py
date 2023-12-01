import json
from pprint import pprint

from src.utils import get_modified_df, load_xlsx_file, get_cards_info, top_five_transactions, get_greeting_phrase, get_converted_date
from src.views import get_stock_prices, get_exchange_rate

if __name__ == '__main__':
    input_date = "2021-10-16 16:00:00"
    with open("../user_settings.json") as json_file:
        data = json.load(json_file)
        user_stocks = data["user_stocks"]
        user_currencies = data["user_currencies"]

    def main_page(date: str) -> dict:
        date_obj = get_converted_date(date)
        selected_df = get_modified_df(load_xlsx_file("../data/operations.xls"), date_obj)
        dict_ = {}
        dict_["greeting"] = get_greeting_phrase()
        dict_["cards"] = get_cards_info(selected_df)
        dict_["top_transactions"] = top_five_transactions(selected_df)
        # dict_["currency_rates"] = get_exchange_rate(user_currencies, date_obj)
        # dict_["stock_prices"] = get_stock_prices(user_stocks, date_obj)
        return dict_


    pprint(main_page(input_date))
