from flask import Flask, jsonify, request, send_from_directory, abort, render_template, url_for, redirect, send_file
from logic.logging_handler import logger
from logic.webhook_handler import webhook_handler
from logic.database_handler import mongo
# from logic.database_handler import
# from logic.encoding_handler import
from logic.general_handler import session_manager
from logic.general_handler import _get_remote_ip
from logic.aws_handler import firehose_generator

import json
import os

app = Flask(__name__)

mongo_host = os.environ['MONGODB_HOST']
mongo_db = os.environ['MONGODB_DB']
mongo_db_dev = os.environ['MONGODB_DB_DEV']
mongo_collection = os.environ['MONGODB_USER_COLLECTION']
mongo_log_collection = os.environ['MONGODB_LOG_COLLECTION']
allowed_tokens = os.environ['API_ALLOWED_TOKENS'].split(',')
use_discord = os.environ['WEBHOOKS_DISCORD_USE_DISCORD']
moderation_urls = os.environ['webhooks']['discord']['moderation_urls']
dev_env = os.environ['DEV']
local_ip = os.environ['GENERAL_LOCAL_IP']

if isinstance(allowed_tokens, str):
    print("The element 'allowed_tokens' should not be a string! Please Update your envs!")
    exit(1)
