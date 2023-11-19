#!/usr/bin/env python3

import json
import logging
import logging.config

from chuvisco import main

logging.config.dictConfig(json.load(open('logging.json')))
logger = logging.getLogger(__name__)

# Run the bot until the user presses Ctrl-C
app = main.create_app()
logger.info('Start polling')
app.run_polling()
