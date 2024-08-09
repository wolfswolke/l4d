from flask import Flask, jsonify, request, send_from_directory, abort, render_template, url_for, redirect, send_file
from logic.logging_handler import logger
from logic.webhook_handler import webhook_handler
from logic.database_handler import mongo
from logic.setup_handler import load_config
# from logic.database_handler import
# from logic.encoding_handler import
from logic.general_handler import session_manager
from logic.general_handler import _get_remote_ip

import json
import os

app = Flask(__name__)

config = load_config()
mongo_host = config['mongodb']['host']
mongo_db = config['mongodb']['db']
mongo_db_dev = config['mongodb']['db_dev']
mongo_collection = config['mongodb']['collection']
allowed_tokens = config['api']['allowed_tokens']
use_discord = config['webhooks']['discord']['use_discord']
moderation_urls = config['webhooks']['discord']['moderation_urls']
dev_env = os.environ['DEV']
local_ip = config['general']['local_ip']

if isinstance(allowed_tokens, str):
    print("The element 'allowed_tokens' should not be a string! Please Update your config!")
    exit(1)
