'''Main module with the aplication creation and all handlers.'''

import logging
import os

import telegram
import telegram.ext

from . import db

logger = logging.getLogger(__name__)


async def save(
    update: telegram.Update,
    *args,  # NOQA: ARG001, ANN002
) -> None:
    '''
    Save the raw message + the timestamp
    '''
    message = db.RawMessage.from_update(update=update)
    with db.create_session() as session:
        session.add(message)
        session.commit()


def create_app() -> telegram.ext.Application:
    '''Create the bot application.'''
    logger.info('Creating app')
    # Create the Application and pass it your bot's token.
    token = os.environ.get('TOKEN', '')
    app = telegram.ext.Application.builder().token(token).build()

    # on non command i.e message - save the message to the database
    save_handler = telegram.ext.MessageHandler(
        telegram.ext.filters.TEXT & ~telegram.ext.filters.COMMAND,
        save,
    )
    app.add_handler(save_handler)
    return app
