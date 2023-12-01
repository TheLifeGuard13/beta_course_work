import pandas as pd
import typing
import datetime


def load_xlsx_file(filename: typing.Any) -> pd.DataFrame:
    """открывает файл в формате xls и превращает в формат DataFrame"""
    try:
        file_data = pd.read_excel(filename, na_filter=False)
    except FileNotFoundError:
        raise FileNotFoundError("Файл не найден")
    return file_data


def get_converted_date(date: str) -> datetime:
    """функция"""
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    return date_obj


def get_modified_df(df: pd.DataFrame, date_obj: datetime) -> pd.DataFrame:
    """фильтрует успешные операции за выбранный месяц"""
    start_date = date_obj.strftime("%Y.%m.01")
    end_date = date_obj.strftime("%Y.%m.%d")
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    modif_df = df.loc[(df["Статус"] == 'OK') & (df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]
    return modif_df


def get_cards_info(modified_df: pd.DataFrame) -> list[dict]:
    """функция"""
    cards_list = list(set([i['Номер карты'] for i in modified_df.to_dict(orient="records") if i['Номер карты']]))
    exit_list = []
    for card in cards_list:
        dict_ = dict()
        df = modified_df[modified_df['Номер карты'] == card]
        summ_ = df.loc[(df['Сумма операции'] < 0) & (df['Валюта операции'] == 'RUB'), 'Сумма операции'].sum()
        dict_['last_digits'] = card[1:]
        dict_['total'] = round(abs(summ_), 2)
        dict_['cashback'] = round(abs(summ_) * 0.01, 2)
        exit_list.append(dict_)
    return exit_list


def top_five_transactions(modified_df: pd.DataFrame) -> list[dict]:
    """функция"""
    df = modified_df.loc[(modified_df['Сумма операции'] < 0) & (modified_df['Валюта операции'] == 'RUB')]
    new_fd = df.loc[df['Номер карты'] != ""]
    top_five_list = new_fd.sort_values(by=["Сумма операции"], ascending=True).head(5).to_dict(orient="records")
    exit_list = []
    for i in top_five_list:
        dict_ = dict().fromkeys(['date', 'amount', 'category', 'description'], None)
        dict_['date'] = pd.Timestamp(i['Дата операции']).strftime('%d.%m.%Y')
        dict_['amount'] = abs(i['Сумма операции'])
        dict_['category'] = i.get('Категория')
        dict_['description'] = i.get('Описание')
        exit_list.append(dict_)
    return exit_list


def get_greeting_phrase() -> str:
    """возвращает приветствие в формате "доброе утро/день/вечер/ночь"
    в зависимости от текущего времени"""
    current_hour = int(datetime.datetime.now().strftime("%H"))
    if current_hour < 6:
        greeting = "Доброе утро"
    elif current_hour < 12:
        greeting = "Добрый день"
    elif current_hour < 18:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"
    return greeting
