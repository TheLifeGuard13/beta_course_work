import os
from pathlib import Path

import pandas as pd
import pytest

from config import OPERATIONS_PATH
from src.reports import report_to_file, spending_by_category
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
