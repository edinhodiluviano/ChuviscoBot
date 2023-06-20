import contextlib
import os

import pytest

from chuvisco import db


@contextlib.contextmanager
def patch_db_dir(new_value: str):
    original_db_dir = os.environ.get('DB_DIR', None)
    os.environ['DB_DIR'] = new_value
    yield
    if original_db_dir is None:
        del os.environ['DB_DIR']
    else:
        os.environ['DB_DIR'] = original_db_dir


@pytest.fixture(scope='function', autouse=True)
def _clear_database():
    yield
    db._create_engine.cache_clear()


@pytest.fixture()
def session():
    with patch_db_dir(''), db.create_session() as session:
        yield session
