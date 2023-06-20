#!/usr/bin/env python3

import logging
import logging.config

from chuvisco import main

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# Run the bot until the user presses Ctrl-C
app = main.create_app()
logger.info('Start polling')
app.run_polling()
