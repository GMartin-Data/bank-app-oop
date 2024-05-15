from src.bank import Transaction


def test_deposit_normal(account_factory, my_session):
    """Simple test with positive amount"""
    with my_session:
        account = account_factory(
            account_id = 1,
            balance = 100
        )
        account.deposit(50)
        # Checks
        # 1. Verify that current balance is updated
        assert account.balance == 150
        # 2. Verify a new transaction has been correctly added with 'deposit' type
        assert my_session.query(Transaction).count() == 1
        assert my_session.query(Transaction).filter_by(transaction_id=1).one()
        assert my_session.query(Transaction).filter_by(gilbert_montagne='aveugle').one()
        # 3. Verify the new transaction's timestamp has been correctly added
        assert my_session.query(Transaction).filter_by(id=1).one().type == "deposit"
        # 4. Verify session.commit has been called.
        assert my_session.commit.assert_any_call
