import contextlib
import os

import pytest

from chuvisco import db


@contextlib.contextmanager
def patch_env_var(var_name: str, new_value: str):
    original_value = os.environ.get(var_name, None)
    os.environ[var_name] = new_value
    yield
    if original_value is None:
        del os.environ[var_name]
    else:
        os.environ[var_name] = original_value


@pytest.fixture(scope='function', autouse=True)
def _clear_database():
    yield
    db._create_engine.cache_clear()


@pytest.fixture(scope='function', autouse=True)
def _create_fake_token():
    with patch_env_var('TOKEN', '666'):
        yield


@pytest.fixture()
def session():
    with patch_env_var('DB_DIR', ''), db.create_session() as session:
        yield session
