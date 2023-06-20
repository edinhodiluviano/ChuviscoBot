import datetime as dt
import random
import string

import pytest
import sqlalchemy as sa
import telegram

from chuvisco import db, main


@pytest.mark.asyncio()
async def test_when_call_save_then_return_none(
    session,  # NOQA: ARG001
):
    update = create_update()
    resp = await main.save(update, None)
    assert resp is None


@pytest.mark.asyncio()
async def test_when_call_save_then_message_table_count_increase_one(session):
    stmt = sa.select(sa.func.count()).select_from(db.Message)
    count_before = session.execute(stmt).scalar()

    update = create_update()
    await main.save(update, None)

    session.commit()
    count_after = session.execute(stmt).scalar()
    assert count_after == count_before + 1


def create_string(length: int = 8) -> str:
    s = random.choices(string.ascii_lowercase, k=length)
    return ''.join(s)


def create_datetime() -> dt.datetime:
    start = dt.datetime(2000, 1, 1, 0, 0, 0, tzinfo=dt.timezone.utc)
    now = dt.datetime.now(tz=dt.timezone.utc)
    interval = (now - start).seconds
    random_delta = random.randint(0, interval)
    return start + dt.timedelta(seconds=random_delta)


def create_user() -> telegram.User:
    user = telegram.User(
        first_name=create_string(),
        id=random.randint(1, 999_999),
        is_bot=False,
        language_code='en',
        username=create_string(),
    )
    return user


def create_chat() -> telegram.Chat:
    chats = [
        telegram.Chat.PRIVATE,
        telegram.Chat.GROUP,
        telegram.Chat.SUPERGROUP,
        telegram.Chat.CHANNEL,
    ]
    chat = telegram.Chat(
        id=random.randint(1, 999_999),
        title=create_string(),
        type=random.choice(chats),
    )
    return chat


def create_update(
    chat: telegram.Chat = None,
    user: telegram.User = None,
) -> telegram.Update:
    if chat is None:
        chat = create_chat()
    if user is None:
        user = create_user()
    update = telegram.Update(
        update_id=random.randint(1, 999_999),
        message=telegram.Message(
            chat=chat,
            date=create_datetime(),
            from_user=user,
            message_id=random.randint(1, 999_999),
            text=create_string(length=99),
        ),
    )
    return update
