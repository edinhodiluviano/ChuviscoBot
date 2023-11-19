'''Main module with the aplication creation and all handlers.'''

import logging
import os
import random
from pathlib import Path

import telegram
import telegram.ext

from . import db

logger = logging.getLogger(__name__)


async def save(
    update: telegram.Update,
    *args,  # NOQA: ARG001, ANN002
) -> None:
    'Save the raw message + the timestamp.'

    message = db.RawMessage.from_update(update=update)
    with db.create_session() as session:
        session.add(message)
        session.commit()


async def hacker(
    update: telegram.Update,
    context: telegram.ext.ContextTypes.DEFAULT_TYPE,  # NOQA: ARG001
) -> None:
    'Send a message when the command /hacker is issued.'

    m = (
        'Quer saber o que é um hacker, o que ele faz e como se tornar um?!\n'
        'aqui é um bom começo: https://garoa.net.br/wiki/Hacker'
    )
    await update.message.reply_text(m)


async def hackear(
    update: telegram.Update,
    context: telegram.ext.ContextTypes.DEFAULT_TYPE,  # NOQA: ARG001
) -> None:
    'Send a message when the command /haquear + "something" is issued.'

    words = update.message.text.split(' ', 1)
    if len(words) == 1:
        this_folder = Path(os.path.realpath(__file__)).parent
        file = this_folder / 'hackear_algo.txt'
        message = file.read_text()
    else:
        videos = [
            'https://www.youtube.com/watch?v=EErY75MXYXI',
            'https://www.youtube.com/watch?v=CNuzEXIAxe8',
            'https://www.youtube.com/watch?v=9_f9Mr10IeI',
            'https://www.youtube.com/watch?v=1MGlTgSnsE4',
            'https://www.youtube.com/watch?v=79vdbA0kth4',
            'https://www.youtube.com/watch?v=AjWfY7SnMBI',
        ]
        video = random.choice(videos)  # NOQA: S311
        message = (
            'Para isso vc precisa decifrar a mensagem secreta escondida '
            f'nesse video: {video}'
        )
    await update.message.reply_text(message)


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

    # on command "/hacker" send a message to the users
    app.add_handler(telegram.ext.CommandHandler('hacker', hacker))

    # on command '/hackear' send a message to the users
    app.add_handler(telegram.ext.CommandHandler('hackear', hackear))

    return app
