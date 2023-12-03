import datetime
import json
import logging
import typing
from pathlib import Path

import pandas as pd

data_path_log = Path(__file__).parent.parent.joinpath("data", "utils.log")
logger = logging.getLogger("__utils__")
file_handler = logging.FileHandler(data_path_log, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def load_xlsx_file(filename: typing.Any) -> pd.DataFrame:
    """конвертирует файл из формата xls в формат pd.DataFrame"""
    try:
        file_data = pd.read_excel(filename, na_filter=False)
        logger.info("Файл успешно преобразован")
        return file_data
    except FileNotFoundError as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции load_xlsx_file()")
        raise error
    except ValueError as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции load_xlsx_file()")
        raise error


def load_json_file(filename: typing.Any) -> typing.Any:
    """конвертирует файл из формата json в формат python"""
    try:
        with open(filename) as json_file:
            file_data = json.load(json_file)
        logger.info("Файл успешно преобразован")
        return file_data
    except FileNotFoundError as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции load_json_file()")
        raise error
    except json.decoder.JSONDecodeError as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции load_json_file()")
        raise error


def get_converted_date(date: str) -> datetime.datetime:
    """преобразовывает дату в формате строки в объект datetime"""
    try:
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        logger.info("Дата успешно преобразована")
        return date_obj
    except ValueError as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции get_converted_date()")
        raise error
    except TypeError as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции get_converted_date()")
        raise error


def filter_operations_by_date(operations: pd.DataFrame, date_obj: datetime.datetime) -> pd.DataFrame:
    """фильтрует успешные операции за месяц, с 1 числа месяца до выбранной даты"""
    try:
        start_date = date_obj.strftime("%Y.%m.01")
        end_date = date_obj.strftime("%Y.%m.%d")
        operations["Дата операции"] = pd.to_datetime(operations["Дата операции"], dayfirst=True)
        filtered_operations = operations.loc[(operations["Статус"] == "OK")
                                             & (operations["Дата операции"] >= start_date)
                                             & (operations["Дата операции"] <= end_date)]
        logger.info("Файл успешно преобразован")
        return filtered_operations
    except ValueError as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции get_modified_df()")
        raise error
    except KeyError as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции get_modified_df()")
        raise error


def get_cards_payments(operations: pd.DataFrame) -> list[dict]:
    """выгружает траты по номеру карт из массива и выдает в формате словарей"""
    try:
        cards_list = list(set([i["Номер карты"] for i in operations.to_dict(orient="records") if i["Номер карты"]]))
        new_list = []
        for card in cards_list:
            new_dict = dict()
            cards_operations = operations[operations["Номер карты"] == card]
            operations_summ = cards_operations.loc[
                (cards_operations["Сумма операции"] < 0)
                & (cards_operations["Валюта операции"] == "RUB"), "Сумма операции"].sum()
            new_dict["last_digits"] = card[1:]
            new_dict["total"] = round(abs(operations_summ), 2)
            new_dict["cashback"] = round(abs(operations_summ) * 0.01, 2)
            new_list.append(new_dict)
        logger.info("Данные по картам успешно выданы")
        return new_list
    except ValueError as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции get_cards_info()")
        raise error
    except KeyError as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции get_cards_info()")
        raise error
    except TypeError as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции get_cards_info()")
        raise error
    except AttributeError as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции get_cards_info()")
        raise error


def get_top_five_operations(operations: pd.DataFrame) -> list[dict]:
    """выгружает топ 5 операций по сумме из массива и выдает в формате словарей"""
    try:
        filtered_operations = operations.loc[(operations["Сумма операции"] < 0)
                                             & (operations["Валюта операции"] == "RUB")]
        card_operations = filtered_operations.loc[filtered_operations["Номер карты"] != ""]
        top_five_operations_list = card_operations.sort_values(by=["Сумма операции"],
                                                               ascending=True).head(5).to_dict(orient="records")
        new_list = []
        for operation in top_five_operations_list:
            new_dict = dict().fromkeys(["date", "amount", "category", "description"], None)
            new_dict["date"] = pd.Timestamp(operation["Дата операции"]).strftime("%d.%m.%Y")
            new_dict["amount"] = abs(operation["Сумма операции"])
            new_dict["category"] = operation.get("Категория")
            new_dict["description"] = operation.get("Описание")
            new_list.append(new_dict)
        logger.info("Данные успешно преобразованы")
        return new_list
    except ValueError as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции top_five_transactions()")
        raise error
    except KeyError as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции top_five_transactions()")
        raise error
    except TypeError as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции top_five_transactions()")
        raise error
    except AttributeError as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции top_five_transactions()")
        raise error


def get_greeting_phrase() -> str:
    """возвращает приветствие в зависимости от текущего времени
    :return: доброе утро/день/вечер/ночь"""
    current_hour = int(datetime.datetime.now().strftime("%H"))
    if current_hour < 6:
        greeting = "Доброй ночи"
    elif current_hour < 12:
        greeting = "Доброе утро"
    elif current_hour < 18:
        greeting = "Добрый день"
    else:
        greeting = "Добрый вечер"
    logger.info("Данные успешно выгружены")
    return greeting
