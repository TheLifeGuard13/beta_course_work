import pandas as pd
import pytest
from pathlib import Path
import os, fnmatch
import datetime

from config import OPERATIONS_PATH
from src.reports import spending_by_category, report_to_file
from src.utils import load_xlsx_file


test_operations_path = Path(__file__).parent.parent.joinpath("tests", "test_data", "test_operations.xls")


@pytest.fixture
def transactions():
    return load_xlsx_file(OPERATIONS_PATH)


def test_spending_by_category(transactions):
    assert spending_by_category(transactions, "Детские товары", "2021-10-15 16:00:00").shape == (4, 15)
    assert spending_by_category(transactions, "Детские товары").shape == (0, 15)
    with pytest.raises(ValueError):
        assert spending_by_category(transactions, "Детские товары", "2021-45-45 16:00:00")


@pytest.fixture
def transactions_test():
    return load_xlsx_file(test_operations_path)


def test_spending_by_category_(transactions_test):
    with pytest.raises(KeyError):
        assert spending_by_category(transactions_test, "Детские товары", "2021-10-15 16:00:00")


def test_report_to_file_with_filename():
    filename = Path(__file__).parent.parent.joinpath("tests", "test_data", "test_report_filename.csv")
    if os.path.exists(filename):
        os.remove(filename)

    @report_to_file(filename=filename)
    def func(df):
        return df

    input_df = func(load_xlsx_file(OPERATIONS_PATH))

    output_df = pd.read_csv(filename, delimiter=",", encoding="utf-8")

    assert input_df.shape == output_df.shape


def test_report_to_file_no_filename():
    @report_to_file()
    def func(df):
        return df

    func(load_xlsx_file(OPERATIONS_PATH))
    file_path = Path(Path(__file__).parent.parent.joinpath("data", "reports"))

    def find(pattern):
        for root, dirs, files in os.walk(os.path.abspath(file_path)):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    return True
                else:
                    return False

    result = find('*_func_report.csv')
    assert result is True
