from bank import Account, Transaction
from db import init_db_connection


def main() -> None:
    engine, Session = init_db_connection(debug=True)

    with Session() as session:
        # Accounts creation
        account1 = Account(session, account_id=1, balance=100)
        account2 = Account(session, account_id=2, balance=50)
        session.add_all([account1, account2])

        # Accounts transfer
        account1.transfer(other=account2, amount=50)

    # Close all connections
    engine.dispose()


if __name__ == "__main__":
    main()
