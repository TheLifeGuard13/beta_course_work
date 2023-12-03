import datetime
import json
import logging
import os
import typing
from pathlib import Path

import pandas as pd

data_path_log = Path(__file__).parent.parent.joinpath("data", "utils.log")
logger = logging.getLogger("__utils__")

if os.path.exists(data_path_log):
    os.remove(data_path_log)

file_handler = logging.FileHandler(data_path_log, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def load_xlsx_file(filename: typing.Any) -> pd.DataFrame:
    """
    открывает файл в формате xls и превращает в формат DataFrame
    :param путь к файлу или строка-адрес
    :return: объект pandas DataFrame
    """
    try:
        file_data = pd.read_excel(filename, na_filter=False)
        logger.info("Файл успешно преобразован")
        return file_data
    except Exception as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции load_xlsx_file()")
        raise error


def load_json_file(filename: typing.Any) -> dict:
    """
    открывает файл в формате json и превращает в формат python
    :param путь к файлу или строка-адрес
    :return: словарь python
    """
    try:
        with open(filename) as json_file:
            data = json.load(json_file)
        logger.info("Файл успешно преобразован")
        return data
    except Exception as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции load_json_file()")
        raise error


def get_converted_date(date: str) -> datetime.datetime:
    """
    преобразовывает дату-строку в объект datetime
    :param: формат "%Y-%m-%d %H:%M:%S"
    :return: объект datetime
    """
    try:
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        logger.info("Дата успешно преобразована")
        return date_obj
    except Exception as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции get_converted_date()")
        raise error


def get_modified_df(df: pd.DataFrame, date_obj: datetime.datetime) -> pd.DataFrame:
    """
    фильтрует успешные операции за выбранный месяц
    :param: объект pandas DataFrame
    :param: объект datetime
    :return: объект pandas DataFrame
    """
    try:
        start_date = date_obj.strftime("%Y.%m.01")
        end_date = date_obj.strftime("%Y.%m.%d")
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
        modif_df = df.loc[
            (df["Статус"] == "OK") & (df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)
        ]
        logger.info("Файл успешно преобразован")
        return modif_df
    except Exception as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции get_modified_df()")
        raise error


def get_cards_info(modified_df: pd.DataFrame) -> list[dict]:
    """выдает траты по номеру карт в формате словарей
    :param: объект pandas DataFrame
    :return: список словарей
    """
    try:
        cards_list = list(set([i["Номер карты"] for i in modified_df.to_dict(orient="records") if i["Номер карты"]]))
        exit_list = []
        for card in cards_list:
            dict_ = dict()
            df = modified_df[modified_df["Номер карты"] == card]
            summ_ = df.loc[(df["Сумма операции"] < 0) & (df["Валюта операции"] == "RUB"), "Сумма операции"].sum()
            dict_["last_digits"] = card[1:]
            dict_["total"] = round(abs(summ_), 2)
            dict_["cashback"] = round(abs(summ_) * 0.01, 2)
            exit_list.append(dict_)
        logger.info("Данные по картам успешно выданы")
        return exit_list
    except Exception as error:
        logger.error(f"Произошла ошибка: {str(error)} в функции get_cards_info()")
        raise error


def top_five_transactions(modified_df: pd.DataFrame) -> list[dict]:
    """выбирает топ 5 операций по размеру трат
    :param: объект pandas DataFrame
    :return: список словарей
    """
    try:
        df = modified_df.loc[(modified_df["Сумма операции"] < 0) & (modified_df["Валюта операции"] == "RUB")]
        new_fd = df.loc[df["Номер карты"] != ""]
        top_five_list = new_fd.sort_values(by=["Сумма операции"], ascending=True).head(5).to_dict(orient="records")
        exit_list = []
        for i in top_five_list:
            dict_ = dict().fromkeys(["date", "amount", "category", "description"], None)
            dict_["date"] = pd.Timestamp(i["Дата операции"]).strftime("%d.%m.%Y")
            dict_["amount"] = abs(i["Сумма операции"])
            dict_["category"] = i.get("Категория")
            dict_["description"] = i.get("Описание")
            exit_list.append(dict_)
        logger.info("Данные успешно преобразованы")
        return exit_list
    except Exception as error:
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
