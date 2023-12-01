import datetime
import logging
import math
import os
from pathlib import Path

from config import OPERATIONS_PATH
from src.utils import load_xlsx_file

data_path_log = Path(__file__).parent.parent.joinpath("data", "services_log.txt")
logger = logging.getLogger("__services__")

if os.path.exists(data_path_log):
    os.remove(data_path_log)

file_handler = logging.FileHandler(data_path_log)
file_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

transactions_dict = load_xlsx_file(OPERATIONS_PATH).to_dict(orient="records")


def invest_copilka(month: str, transactions: list[dict[str, any]], limit: int = None) -> float:
    """рассчитывает сумму в копилке путем округления платежей за выбранный срок с выбранным лимитом
    :param месяц в формате "YYYY-MM"
    :param список словарей
    :param лимит
    :return сумма в копилке"""
    money_in_copilka = 0
    date_obj = datetime.datetime.strptime(month, "%Y-%m")
    corr_month = date_obj.strftime("%m.%Y")
    required_trans = [
        transaction
        for transaction in transactions
        if corr_month in transaction["Дата операции"] and transaction["Сумма платежа"] == "OK"
    ]
    for transaction in required_trans:
        if transaction["Сумма платежа"] < 0 and abs(int(transaction["Сумма платежа"])) % limit != 0:
            transaction["Сумма платежа"] = abs(transaction["Сумма платежа"])
            if limit == 50:
                rounded_amount = math.ceil(transaction["Сумма платежа"] / 100) * 100
                difference = rounded_amount - transaction["Сумма платежа"] - limit
                if difference <= 0:
                    round_amount = rounded_amount - transaction["Сумма платежа"]
                else:
                    round_amount = difference
            else:
                round_amount = math.ceil(transaction["Сумма платежа"] / limit) * limit - transaction["Сумма платежа"]
            money_in_copilka += round_amount
    logger.info("Операции выгружены успешно")
    return round(money_in_copilka, 2)


print(invest_copilka("2021-10", transactions_dict, 50))
