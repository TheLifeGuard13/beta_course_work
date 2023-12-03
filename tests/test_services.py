from pathlib import Path

import pytest

from config import OPERATIONS_PATH
from src.services import invest_copilka
from src.utils import load_xlsx_file

test_operations_path = Path(__file__).parent.parent.joinpath("tests", "test_data", "test_operations.xls")


@pytest.fixture
def transactions():
    df = load_xlsx_file(OPERATIONS_PATH)
    transactions_dict = df.to_dict(orient="records")
    return transactions_dict


def test_invest_copilka(transactions):
    assert invest_copilka("2021-10", transactions, 10) == 530.62
    assert invest_copilka("2021-10", transactions, 50) == 4166.75
    assert invest_copilka("2021-10", transactions, 100) == 8415.4
    assert invest_copilka("2023-10", transactions, 100) == 0
    with pytest.raises(ValueError):
        assert invest_copilka("2024-13", transactions, 100)


@pytest.fixture
def transactions_test():
    df = load_xlsx_file(test_operations_path)
    transactions_dict = df.to_dict(orient="records")
    return transactions_dict


def test_invest_copilka_(transactions_test):
    with pytest.raises(KeyError):
        assert invest_copilka("2021-10", transactions_test, 100)
