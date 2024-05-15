from mock_alchemy.mocking import AlchemyMagicMock
import pytest

from src.bank import Account


@pytest.fixture
def account_factory():
    def create_account(session, account_id, balance):
        return Account(
            session = AlchemyMagicMock(),
            account_id = account_id,
            balance = balance
        )
    return create_account
