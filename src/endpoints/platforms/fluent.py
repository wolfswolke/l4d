import base64
import io

from flask_definitions import *
import re

from logic.date_handler import get_current_date

# respond_with_empty_img
# Responds with an empty GIF image of 1x1 pixel (rather than an empty string).

# use_204_response
# Respond status code with 204

# INPUT TYPES
# Content-Type: application/json
# Content-Type: application/ndjson
# Content-Type: application/msgpack
# OTHER supported types:
# Media Types	            data format 	version
# application/json          JSON            -
# application/csp-report    JSON            1.17.0
# application/msgpack       MessagePack     -
# application/x-ndjson      NDJSON          1.14.5

temp_logs = []

def sanitize_log_message(message_bytes):
    """
    Sanitizes a log message to remove sensitive information and ensure it is safe for logging.
    """
    # Remove URLs with credentials
    message = message_bytes.decode('utf-8', errors='replace')
    message = re.sub(r'https?://[^/]+:[^@]+@', 'https://<CREDENTIALS_REMOVED>@', message)

    # Replace new lines and other control characters
    message = message.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

    # Escape or remove any potentially dangerous characters
    safe_message = re.sub(r'[^\x20-\x7E]', '', message)  # Removes non-printable ASCII characters

    # Remove h3 colon and semicolon
    pattern = r'(alt-svc:\s*h3="[^"]*?)\s*";'
    safe_message = re.sub(pattern, r'\1";', safe_message)

    # Remove Response Header with URLS
    safe_message = safe_message.replace('{"endpoints":[{"url":"', "")
    safe_message = safe_message.replace('"}],"group":"cf-nel","max_age":604800}', "")
    safe_message = safe_message.replace('NEL: {"success_fraction":0,"report_to":"cf-nel","max_age":604800}', "")
    pattern = r'"log": ".*? Response Header.*?"\n?'
    safe_message = re.sub(pattern, '', safe_message, flags=re.DOTALL)
    pattern = re.compile(r'"log": "(?:[^\\"]|\\\\|\\")*[^}]*[^"]*"[A-Za-z0-9]+":"[^"]*","[^"]*"[^"]*"', re.IGNORECASE)
    # Like AAAAAAA how tf?????
    # How can a string be this fucked up?!?!?!?!
    # Problematic section of the string: 'Header alt-svc: h3=":443"; ma=86400"}]'
    safe_message = pattern.sub('', safe_message)
    try:
        dat = json.loads(safe_message)
        print(dat)
        print("No error")
    except json.JSONDecodeError as e:
        error_position = e.pos
        start = max(0, error_position - 20)
        end = min(len(safe_message), error_position + 20)
        snippet = safe_message[start:end]
        print(f"JSONDecodeError: {e}")
        print(f"Problematic section of the string: '{snippet}'")

    except Exception as e:
        print(e)

    return safe_message


def json_log_validator(data):
    # OLD CODE
    cleaned_str = data.decode('utf8')
    # base_str = cleaned_str.replace('\n', '')
    cleaned_str = cleaned_str.replace('://', '-')
    cleaned_str = cleaned_str.replace('"https', 'https')
    # cleaned_str = cleaned_str.replace('""', '"')
    cleaned_str = cleaned_str.replace('\\', '\\\\')
    cleaned_str = cleaned_str.replace(u"\u000D", "")  # Carriage Return
    cleaned_str = cleaned_str.replace(u"\u000A", "")  # Line Feed
    cleaned_str = cleaned_str.replace(u"\u0009", "")  # Horizontal Tab
    cleaned_str = cleaned_str.replace('{""', "{")
    cleaned_str = cleaned_str.replace('"":', ":")
    cleaned_str = cleaned_str.replace('"url"', "url")
    cleaned_str = cleaned_str.replace('"endpoints"', "endpoints")
    cleaned_str = cleaned_str.replace('"}],', "}]")
    cleaned_str = cleaned_str.replace('"group"', "group")
    cleaned_str = cleaned_str.replace('"cf-nel"', "cf-nel")
    cleaned_str = cleaned_str.replace('"max_age"', "max_age")
    cleaned_str = cleaned_str.replace('"report_to"', "report_to")
    cleaned_str = cleaned_str.replace('"success_fraction"', "success_fraction")
    cleaned_str = cleaned_str.replace('":443"', ":443")
    return cleaned_str


def respond_with_empty_img():
    gif = 'R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='
    gif_str = base64.b64decode(gif)
    return send_file(io.BytesIO(gif_str), mimetype='image/gif')


def get_credentials():
    try:
        auth = request.authorization
        if auth is None:
            return None
        if auth.username is None or auth.password is None:
            return None
        if auth.username == "" or auth.password == "":
            return None
        # todo validate
        logger.log(level="info", handler="fluentd", content=f"username: {auth.username} password: {auth.password}")
    except KeyError:
        return None


@app.route('/api/v1/fluentd/empty/<index>', methods=['POST'])
def fluentd_empty(index):
    try:
        get_credentials()
        data = request.data
        cleaned_str = sanitize_log_message(data)
        logger.log(level="info", handler="fluentd", content=f"index: {index} data: {json.loads(cleaned_str)}")
        log_obj = {"index": index,
                   "time": get_current_date(),
                   "data": json.loads(cleaned_str),
                   "response": "empty"}
        mongo.add_log("fluent", log_obj)
        return "", 204
    except json.JSONDecodeError as e:
        logger.log_exception(e)
        # TEMP workaround for shitty JSON...
        return jsonify(""), 204
    except Exception as e:
        logger.log_exception(e)
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500


@app.route('/api/v1/fluentd/gif/<index>', methods=['POST'])
def fluentd_gif(index):
    try:
        get_credentials()
        data = request.data
        cleaned_str = sanitize_log_message(data)
        logger.log(level="info", handler="fluentd", content=f"index: {index} data: {json.loads(cleaned_str)}")
        log_obj = {"index": index,
                   "time": get_current_date(),
                   "data": json.loads(cleaned_str),
                   "response": "gif"}
        mongo.add_log("fluent", log_obj)
        return respond_with_empty_img()
    except Exception as e:
        logger.log_exception(e)
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500


@app.route('/temp/fluentd', methods=['GET'])
def temp_logview():
    return jsonify(temp_logs)
