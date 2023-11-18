'''Database module with the session creator and all models.'''

import contextlib
import datetime as dt
import functools
import logging
import os
import pathlib

import sqlalchemy as sa
import sqlalchemy.orm
import telegram

logger = logging.getLogger(__name__)
Base = sa.orm.declarative_base()


def _get_db_url() -> str:
    db_dir = os.environ.get('DB_DIR', '')
    if db_dir == '':  # NOQA: PLC1901
        return 'sqlite://'
    db_dir = pathlib.Path(db_dir)
    db_file = db_dir.absolute() / 'chuvisco_db.sqlite'
    return 'sqlite:///' + str(db_file)


@functools.cache
def _create_engine() -> sa.engine.base.Engine:
    url = _get_db_url()
    msg = f'Initializing sqlite database in file "{url}"'
    logger.debug(msg)
    engine = sa.create_engine(
        url,
        connect_args={'check_same_thread': False},
        poolclass=sa.pool.StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    return engine


@contextlib.contextmanager
def create_session() -> sa.orm.Session:
    '''
    Create a syncronous session for the sqlite database.

    To be used inside `with` blocks.
    '''
    engine = _create_engine()
    session_local = sa.orm.sessionmaker(
        autocommit=False, autoflush=False, bind=engine,
    )
    session = session_local()
    try:
        yield session
    finally:
        session.close()


class RawMessage(Base):
    '''A telegram message saved in the database.'''

    __tablename__ = 'message'

    id = sa.Column(sa.Integer, primary_key=True)  # NOQA: A003
    timestamp = sa.Column(sa.DateTime, index=True, nullable=False)
    message = sa.Column(sa.JSON, index=False)

    @classmethod
    def from_update(
        cls,  # NOQA: ANN102
        update: telegram.Update,
    ) -> 'RawMessage':
        'Create an instace of a message from an Update.'
        obj = cls(
            timestamp=dt.datetime.now(tz=dt.timezone.utc),
            message=update.message.to_dict(),
        )
        return obj
