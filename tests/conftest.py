from mock_alchemy.mocking import UnifiedAlchemyMagicMock
import pytest

from src.bank import Account


@pytest.fixture
def my_session():
    session = UnifiedAlchemyMagicMock()
    yield session
    session.rollback()

@pytest.fixture
def account_factory(my_session):
    def create_account(account_id, balance):
        new_account = Account(
            session = my_session,
            account_id = account_id,
            balance = balance
        )
        my_session.add(new_account)
        my_session.commit()
        return new_account
    return create_account
