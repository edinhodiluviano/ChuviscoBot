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


class Message(Base):
    '''A telegram message saved in the database.'''

    __tablename__ = 'message'

    id = sa.Column(sa.Integer, primary_key=True)  # NOQA: A003
    timestamp = sa.Column(sa.DateTime, index=True, nullable=False)
    text = sa.Column(sa.String, index=False)
    channel_id = sa.Column(sa.Integer, index=True)
    channel_title = sa.Column(sa.String, index=False)
    sender_user_id = sa.Column(sa.Integer, index=True)
    sender_first_name = sa.Column(sa.String, index=False)
    sender_username = sa.Column(sa.String, index=False)

    @classmethod
    def from_update(
        cls,  # NOQA: ANN102
        update: telegram.Update,
    ) -> 'Message':
        'Create an instace of a message from an Update.'
        obj = cls(
            timestamp=dt.datetime.now(tz=dt.timezone.utc),
            text=update.message.text,
            channel_id=update.message.chat.id,
            channel_title=update.message.chat.title,
            sender_user_id=update.message.from_user.id,
            sender_first_name=update.message.from_user.first_name,
            sender_username=update.message.from_user.username,
        )
        return obj
