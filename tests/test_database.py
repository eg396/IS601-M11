## test_database.py
## IS 601 Module 11
## Evan Garvey

from app.database_init import drop_db, init_db
import pytest
from sqlalchemy.exc import SQLAlchemyError
from app.database import get_db, get_engine

def test_get_engine_invalid_url():
    invalid_url = "not_a_valid_db_url"

    with pytest.raises(SQLAlchemyError):
        get_engine(database_url=invalid_url)

def test_get_db_closes_session():
    # Create the generator
    db_gen = get_db()

    # Get the session from the generator
    db = next(db_gen)
    assert db is not None  # The session should be a valid object

    # Finish the generator (this triggers the 'finally' block to close the session)
    try:
        next(db_gen)
    except StopIteration:
        pass  # Expected, since get_db only yields once

def test_init_and_drop_db():
    try:
        init_db()
        drop_db()
    except Exception as e:
        assert False, f"Unexpected error during init/drop db: {e}"