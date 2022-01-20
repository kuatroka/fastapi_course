import imp
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds
import pytest


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [(3, 2, 5), (7, 1, 8),
                                                  (34, 34, 68)])
def test_add(num1, num2, expected):
    print("testing add function")
    assert add(num1, num2) == expected


def test_subtract():
    print("testing subtract function")

    assert subtract(2, 3) == -1


def test_multiply():
    print("testing multiply function")

    assert multiply(2, 3) == 6


def test_divide():
    print("testing divide function")

    assert divide(20, 5) == 4


def test_bank_set_initial_account(bank_account):

    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):

    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):

    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_deposit(bank_account):

    bank_account.deposit(20)
    assert bank_account.balance == 70


def test_interest(bank_account):

    bank_account.collect_interest()
    assert round(bank_account.balance, 5) == 55


@pytest.mark.parametrize("deposited, withdrawn, expected", [(200, 100, 100),
                                                            (50, 10, 40),
                                                            (1100, 200, 900)])
def test_bank_transaction(zero_bank_account, deposited, withdrawn, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrawn)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)


# test_add()
