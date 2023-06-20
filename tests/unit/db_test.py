import sqlalchemy as sa

from chuvisco import db

from .conftest import patch_db_dir


def test_given_test_env_when_create_session_then_can_execute_query(
    session,  # NOQA: ARG001
):
    stmt = sa.text('SELECT 1')
    with db.create_session() as session_:
        r = session_.execute(stmt).scalar()
    assert r == 1


def test_given_temp_dir_when_create_session_then_can_execute_query(tmp_path):
    with patch_db_dir(str(tmp_path)):
        stmt = sa.text('SELECT 1')
        with db.create_session() as session_:
            r = session_.execute(stmt).scalar()
        assert r == 1


def test_given_temp_dir_when_create_session_then_db_file_is_created(tmp_path):
    with patch_db_dir(str(tmp_path)):
        with db.create_session() as session:
            session.commit()
        db_file = tmp_path / 'chuvisco_db.sqlite'
        assert db_file.exists()
