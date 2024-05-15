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
        assert (my_session
                .query(Transaction)
                .filter(Transaction.transaction_id == 1)  # Maybe too picky and not needed
                .one()
                ).type == "deposit"
        # 3. Verify the new transaction's timestamp has been correctly added
        assert (my_session
                .query(Transaction)
                .filter(Transaction.transaction_id == 1)  # Maybe too picky and not needed
                .one()
                ).timestamp
        # 4. Verify session.commit has been called.
        assert my_session.commit.call_count == 2
        # my_session.commit.assert_any_call()
        # The non-commented is better as `session.commit` is also called within account_factory

def test_deposit_negative_amount(account_factory, my_session):
    with my_session:
        account = account_factory(
            account_id = 1,
            balance = 100
        )
        account.deposit(-50)
        # Checks
        # 1. Verify the account balance hasn't changed
        assert account.balance == 100
        # 2. Verify no transaction was created
        assert my_session.query(Transaction).count() == 0
        # 3. Verify that session.commit wasn't called
        assert my_session.commit.call_count == 1

def test_deposit_zero_amount(account_factory, my_session):
    with my_session:
        account = account_factory(
            account_id = 1,
            balance = 100
        )
        account.deposit(0)
        # Checks
        # 1. Verify the account balance hasn't changed
        assert account.balance == 100
        # 2. Verify no transaction was created
        assert my_session.query(Transaction).count() == 0
        # 3. Verify that session.commit wasn't called
        assert my_session.commit.call_count == 1

def test_withdraw_normal(account_factory, my_session):
    with my_session:
        account = account_factory(
            account_id = 1,
            balance = 100
        )
        account.withdraw(30)
        # Checks
        # 1. Verify the account balance is correctly updated
        assert account.balance == 70
        # 2. Verify a new transaction has been correctly added with 'withdraw' type
        assert my_session.query(Transaction).count() == 1
        assert (my_session
                .query(Transaction)
                .filter(Transaction.transaction_id == 1)  # Maybe too picky and not needed
                .one()
                ).type == "withdraw"
        # 4. Verify session.commit has been called.
        assert my_session.commit.call_count == 2

def test_withdraw_insufficient_funds(account_factory, my_session):
    with my_session:
        account = account_factory(
            account_id = 1,
            balance = 100
        )
        account.withdraw(200)
        # Checks
        # 1. Verify the account balance remains unchanged
        assert account.balance == 100
        # 2. Verify no transaction was created
        assert my_session.query(Transaction).count() == 0
        # 3. Verify that session.commit wasn't called
        assert my_session.commit.call_count == 1

def test_withdraw_negative_amount(account_factory, my_session):
    with my_session:
        account = account_factory(
            account_id = 1,
            balance = 100
        )
        account.withdraw(-300)
        # Checks
        # 1. Verify the account balance remains unchanged
        assert account.balance == 100
        # 2. Verify no transaction was created
        assert my_session.query(Transaction).count() == 0
        # 3. Verify that session.commit wasn't called
        assert my_session.commit.call_count == 1

def test_withdraw_zero_amount(account_factory, my_session):
    with my_session:
        account = account_factory(
            account_id = 1,
            balance = 100
        )
        account.withdraw(0)
        # Checks
        # 1. Verify the account balance remains unchanged
        assert account.balance == 100
        # 2. Verify no transaction was created
        assert my_session.query(Transaction).count() == 0
        # 3. Verify that session.commit wasn't called
        assert my_session.commit.call_count == 1

def test_transfer_normal(account_factory, my_session):
    with my_session:
        account1 = account_factory(
            account_id = 1,
            balance = 100
        )
        account2 = account_factory(
            account_id = 1,
            balance = 50
        )
        account1.transfer(account2, 20)
        # Checks
        # 1. Verify the amount is deduced from the source account's balance
        assert account1.balance == 80
        # 2. Verify the amount is added to the destination account's balance
        assert account2.balance == 70
        # 3. Verify two transactions are created with the appropriate types
        assert my_session.query(Transaction).count() == 2
        results = (my_session
                   .query(Transaction)
                   .all())
        # WARNING: There's a weird error when
        # filtering by transaction_id and using .one()
        assert results[0].type == "withdraw" and results[1].type == "deposit"
        # 4. Verify session.commit has been called
        assert my_session.commit.call_count == 3  # 2 for accounts, 1 for both transactions

def test_transfer_insufficient_funds(account_factory, my_session):
    with my_session:
        account1 = account_factory(
            account_id = 1,
            balance = 100
        )
        account2 = account_factory(
            account_id = 1,
            balance = 50
        )
        account1.transfer(account2, 200)
        # Checks
        # 1. Verify both accounts' balance remain unchanged
        assert account1.balance == 100 and account2.balance == 50
        # 2. Verify no transaction was added
        assert my_session.query(Transaction).count() == 0
        # 3. Verify that session.commit wasn't called
        assert my_session.commit.call_count == 2  # One for each account        

def test_transfer_negative_amount(account_factory, my_session):
    with my_session:
        account1 = account_factory(
            account_id = 1,
            balance = 100
        )
        account2 = account_factory(
            account_id = 1,
            balance = 50
        )
        account1.transfer(account2, -200)
        # Checks
        # 1. Verify both accounts' balance remain unchanged
        assert account1.balance == 100 and account2.balance == 50
        # 2. Verify no transaction was added
        assert my_session.query(Transaction).count() == 0
        # 3. Verify that session.commit wasn't called
        assert my_session.commit.call_count == 2  # One for each account

def test_transfer_zero_amount(account_factory, my_session):
    with my_session:
        account1 = account_factory(
            account_id = 1,
            balance = 100
        )
        account2 = account_factory(
            account_id = 1,
            balance = 50
        )
        account1.transfer(account2, 0)
        # Checks
        # 1. Verify both accounts' balance remain unchanged
        assert account1.balance == 100 and account2.balance == 50
        # 2. Verify no transaction was added
        assert my_session.query(Transaction).count() == 0
        # 3. Verify that session.commit wasn't called
        assert my_session.commit.call_count == 2  # One for each account
