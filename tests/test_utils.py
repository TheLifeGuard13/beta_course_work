import pytest
from pathlib import Path
import datetime
from freezegun import freeze_time

from config import OPERATIONS_PATH, STOCKS_CURRENCIES_PATH
from src.utils import load_xlsx_file, load_json_file, get_converted_date, get_modified_df, get_cards_info, \
    top_five_transactions, get_greeting_phrase

empty_operations_path = Path(__file__).parent.parent.joinpath("tests", "test_data", "empty_operations.xls")
test_operations_path = Path(__file__).parent.parent.joinpath("tests", "test_data", "test_operations.xls")
test_date = "2021-10-16 16:00:00"


def test_load_xlsx_file():
    assert load_xlsx_file(OPERATIONS_PATH).shape == (6705, 15)
    assert load_xlsx_file(test_operations_path).shape == (6705, 6)
    with pytest.raises(FileNotFoundError):
        assert load_xlsx_file("../src/no_file.xls")
    with pytest.raises(ValueError):
        assert load_xlsx_file(empty_operations_path)


def test_load_json_file():
    assert len(load_json_file(STOCKS_CURRENCIES_PATH)) == 2
    with pytest.raises(FileNotFoundError):
        assert load_json_file("./src/test_json.json")


def test_get_converted_date():
    assert get_converted_date(test_date) == datetime.datetime(2021, 10, 16, 16)
    with pytest.raises(ValueError):
        assert get_converted_date("2021.10.16")


def test_get_modified_df():
    assert len(get_modified_df(load_xlsx_file(OPERATIONS_PATH), get_converted_date(test_date))) == 91
    with pytest.raises(ValueError):
        assert get_modified_df(load_xlsx_file(test_operations_path), get_converted_date(test_date))
    with pytest.raises(KeyError):
        assert get_modified_df(load_xlsx_file(empty_operations_path), get_converted_date(test_date))


def test_get_cards_info():
    assert len(get_cards_info(load_xlsx_file(OPERATIONS_PATH))) == 7
    with pytest.raises(KeyError):
        assert get_cards_info(load_xlsx_file(empty_operations_path))


def test_top_five_transactions():
    assert len(top_five_transactions(load_xlsx_file(OPERATIONS_PATH))) == 5
    with pytest.raises(KeyError):
        assert top_five_transactions(load_xlsx_file(empty_operations_path))


@freeze_time("2021-10-16 03:00:00")
def test_get_greeting_phrase_morn():
    assert get_greeting_phrase() == "Доброе утро"


@freeze_time("2021-10-16 10:00:00")
def test_get_greeting_phrase_day():
    assert get_greeting_phrase() == "Добрый день"


@freeze_time("2021-10-16 15:00:00")
def test_get_greeting_phrase_eve():
    assert get_greeting_phrase() == "Добрый вечер"


@freeze_time("2021-10-16 21:00:00")
def test_get_greeting_phrase_night():
    assert get_greeting_phrase() == "Доброй ночи"
