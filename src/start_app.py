"""

"""
# ------------------------------------------------------- #
# imports
# ------------------------------------------------------- #
from threading import Thread
import time
from waitress import serve

from flask_definitions import *
import endpoints.user
import endpoints.general

import endpoints.platforms.aws
import endpoints.platforms.fluent

# ------------------------------------------------------- #
# functions
# ------------------------------------------------------- #


def run():
    serve(app, host='0.0.0.0', port=8080, threads=100, connection_limit=2000, cleanup_interval=50, channel_timeout=190,)


def keep_alive():
    try:
        if dev_env == "true":
            logger.log(level="boot", handler="api", content={"event": "api started in dev mode."})
        else:
            logger.log(level="boot", handler="api", content={"event": "api started."})
        t = Thread(target=run)
        t.daemon = True
        t.start()
        while True:
            time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        print('Received keyboard interrupt, quitting threads.')
        logger.log(level="boot", handler="api", content={"event": "api stopped."})


# ------------------------------------------------------- #
# global variables
# ------------------------------------------------------- #


# ------------------------------------------------------- #
# main
# ------------------------------------------------------- #
webhook_handler.setup(discord_urls=moderation_urls, use_discord=use_discord)
session_manager.setup()
if dev_env == "true":
    mongo.setup(mongo_host, mongo_db_dev, mongo_collection)
else:
    mongo.setup(mongo_host, mongo_db, mongo_collection)
# todo Add some db stuff here...
firehose_generator.setup("00000000-0000-0000-0000-000000000000")
keep_alive()
