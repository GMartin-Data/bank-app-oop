"""
This file contains all the logic devoted to manage the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .bank import Base


def init_db_connection(debug=False):
    # It seems safer to return both even if you will mainly use
    # context managers like `with session:`
    # You will have to close all with `engine.dispose()`.
    engine = create_engine("sqlite:///bank.db", echo=debug)
    Base.metadata.create_all(engine)  # This always checks if table already exists beforehand
    return engine, sessionmaker(bind=engine)
