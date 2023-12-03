import datetime
import logging
import math
from pathlib import Path

data_path_log = Path(__file__).parent.parent.joinpath("data", "services.log")
logger = logging.getLogger("__services__")
file_handler = logging.FileHandler(data_path_log, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def invest_copilka(month: str, transactions: list[dict], limit: int) -> float:
    """рассчитывает сумму в копилке путем округления платежей за выбранный срок с выбранным лимитом"""
    money_in_copilka = 0
    try:
        date_obj = datetime.datetime.strptime(month, "%Y-%m")
        corr_month = date_obj.strftime("%m.%Y")
        required_transactions = [
            transaction
            for transaction in transactions
            if corr_month in transaction["Дата операции"] and transaction["Статус"] == "OK"
        ]
        for transaction in required_transactions:
            if transaction["Сумма платежа"] < 0 and abs(int(transaction["Сумма платежа"])) % limit != 0:
                payment_amount = abs(transaction["Сумма платежа"])
                if limit == 50:
                    rounded_amount = math.ceil(payment_amount / 100) * 100
                    difference = rounded_amount - payment_amount - limit
                    if difference <= 0:
                        round_amount = rounded_amount - payment_amount
                    else:
                        round_amount = difference
                elif limit == 10 or limit == 100:
                    round_amount = math.ceil(payment_amount / limit) * limit - payment_amount
                else:
                    round_amount = 0
                money_in_copilka += round_amount
        logger.info("Копилка успешно наполнена")
        return round(money_in_copilka, 2)
    except ValueError as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции invest_copilka()")
        raise error
    except KeyError as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции invest_copilka()")
        raise error
    except TypeError as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции invest_copilka()")
        raise error
