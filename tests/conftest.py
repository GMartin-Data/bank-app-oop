from mock_alchemy.mocking import UnifiedAlchemyMagicMock
import pytest

from src.bank import Account


@pytest.fixture
def my_session():
    return UnifiedAlchemyMagicMock()

@pytest.fixture
def account_factory():
    def create_account(account_id, balance, session):
        return Account(
            session = session,
            account_id = account_id,
            balance = balance
        )
    return create_account
