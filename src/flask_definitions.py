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
CLOUDFLARE_CSP = {
    'default-src': "'self'",
    'script-src': [
        "'self'",
        "'unsafe-inline'",
        "*.cloudflare.com",
        "*.cloudflareinsights.com",
    ],
    'style-src': [
        "'self'",
        "'unsafe-inline'",
        "*.cloudflare.com",
    ],
    'img-src': [
        "'self'",
        "data:",
        "*.cloudflare.com",
    ],
    'connect-src': [
        "'self'",
        "*.cloudflare.com",
    ],
    'form-action': "'self'",
    'frame-ancestors': "'none'",
}

def compile_csp():
    return '; '.join(
        f"{key} {' '.join(value)}"
        for key, value in CLOUDFLARE_CSP.items()
    )

@app.after_request
def add_security_headers(response):
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    response.headers['Cross-Origin-Resource-Policy'] = 'same-origin'
    response.headers['Content-Security-Policy'] = compile_csp()
    response.headers['Permissions-Policy'] = (
        "accelerometer=(), ambient-light-sensor=(), autoplay=(), "
        "battery=(), camera=(), display-capture=(), document-domain=(), "
        "encrypted-media=(), execution-while-not-rendered=(), "
        "execution-while-out-of-viewport=(), fullscreen=(), "
        "geolocation=(), gyroscope=(), magnetometer=(), microphone=(), "
        "midi=(), navigation-override=(), payment=(), "
        "picture-in-picture=(), publickey-credentials-get=(), "
        "screen-wake-lock=(), sync-xhr=(), usb=(), "
        "web-share=(), xr-spatial-tracking=()"
    )
    response.headers['X-Forwarded-Proto'] = 'https'
    return response

@app.route('/csp-violation-report', methods=['POST'])
def csp_report():
    app.logger.warning(f"CSP violation: {request.data}")
    return '', 204

mongo_host = os.environ['MONGODB_HOST']
mongo_db = os.environ['MONGODB_DB']
mongo_db_dev = os.environ['MONGODB_DB_DEV']
mongo_collection = os.environ['MONGODB_USER_COLLECTION']
mongo_log_collection = os.environ['MONGODB_LOG_COLLECTION']
allowed_tokens = os.environ['API_ALLOWED_TOKENS'].split(',')
use_discord = os.environ['WEBHOOKS_DISCORD_USE_DISCORD']
moderation_urls = os.environ['WEBHOOKS_DISCORD_MODERATION_URLS']
dev_env = os.environ['DEV']
local_ip = os.environ['GENERAL_LOCAL_IP']

if isinstance(allowed_tokens, str):
    print("The element 'allowed_tokens' should not be a string! Please Update your envs!")
    exit(1)
