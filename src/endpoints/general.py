from flask import redirect

from flask_definitions import *


@app.route('/', methods=["GET"])
def index():
    # Add stuff in that page
    return render_template("index.html")


@app.route('/robots.txt', methods=["GET"])
def robots():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/.well-known/security.txt', methods=["GET"])
def security():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/.well-known/gpc.json', methods=["GET"])
def gpc():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/.well-known/dnt-policy.txt', methods=["GET"])
def dnt():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/favicon.ico')
def favicon():
    try:
        return send_from_directory(os.path.join(app.root_path, 'image'), 'favicon.ico',
                                   mimetype='image/vnd.microsoft.icon')
    except TimeoutError:
        return jsonify({"status": "Timeout"}), 408
    except Exception as e:
        print(e)
        return jsonify({"status": "Unknown Error"}), 500


@app.route('/apple-touch-icon.png')
def apple_touch_icon():
    try:
        return send_from_directory(os.path.join(app.root_path, 'image'), 'apple-touch-icon.png',
                                   mimetype='image/vnd.microsoft.icon')
    except TimeoutError:
        return jsonify({"status": "Timeout"}), 408
    except Exception as e:
        print(e)
        return jsonify({"status": "Unknown Error"}), 500


@app.route('/android-chrome-192x192.png')
def android_chrome_192x192():
    try:
        return send_from_directory(os.path.join(app.root_path, 'image'), 'android-chrome-192x192.png',
                                   mimetype='image/vnd.microsoft.icon')
    except TimeoutError:
        return jsonify({"status": "Timeout"}), 408
    except Exception as e:
        print(e)
        return jsonify({"status": "Unknown Error"}), 500


@app.route('/android-chrome-256x256.png')
def android_chrome_256x256():
    try:
        return send_from_directory(os.path.join(app.root_path, 'image'), 'android-chrome-256x256.png',
                                   mimetype='image/vnd.microsoft.icon')
    except TimeoutError:
        return jsonify({"status": "Timeout"}), 408
    except Exception as e:
        print(e)
        return jsonify({"status": "Unknown Error"}), 500


@app.route('/browserconfig.xml')
def browserconfig():
    try:
        return send_from_directory(os.path.join(app.root_path, 'image'), 'browserconfig.xml')
    except TimeoutError:
        return jsonify({"status": "Timeout"}), 408
    except Exception as e:
        print(e)
        return jsonify({"status": "Unknown Error"}), 500


@app.route('/favicon-16x16.png')
def favicon_16x16():
    try:
        return send_from_directory(os.path.join(app.root_path, 'image'), 'favicon-16x16.png',
                                   mimetype='image/vnd.microsoft.icon')
    except TimeoutError:
        return jsonify({"status": "Timeout"}), 408
    except Exception as e:
        print(e)
        return jsonify({"status": "Unknown Error"}), 500


@app.route('/favicon-32x32.png')
def favicon_32x32():
    try:
        return send_from_directory(os.path.join(app.root_path, 'image'), 'favicon-32x32.png',
                                   mimetype='image/vnd.microsoft.icon')
    except TimeoutError:
        return jsonify({"status": "Timeout"}), 408
    except Exception as e:
        print(e)
        return jsonify({"status": "Unknown Error"}), 500


@app.route('/favicon.png')
def favicon_png():
    try:
        return send_from_directory(os.path.join(app.root_path, 'image'), 'favicon.png',
                                   mimetype='image/vnd.microsoft.icon')
    except TimeoutError:
        return jsonify({"status": "Timeout"}), 408
    except Exception as e:
        print(e)
        return jsonify({"status": "Unknown Error"}), 500


@app.route('/mstile-150x150.png')
def mstile_150x150():
    try:
        return send_from_directory(os.path.join(app.root_path, 'image'), 'mstile-150x150.png',
                                   mimetype='image/vnd.microsoft.icon')
    except TimeoutError:
        return jsonify({"status": "Timeout"}), 408
    except Exception as e:
        print(e)
        return jsonify({"status": "Unknown Error"}), 500


@app.route('/safari-pinned-tab.svg')
def safari_pinned_tab():
    try:
        return send_from_directory(os.path.join(app.root_path, 'image'), 'safari-pinned-tab.svg',
                                   mimetype='image/svg+xml')
    except TimeoutError:
        return jsonify({"status": "Timeout"}), 408
    except Exception as e:
        print(e)
        return jsonify({"status": "Unknown Error"}), 500


@app.route('/site.webmanifest')
def site_webmanifest():
    try:
        return send_from_directory(os.path.join(app.root_path, 'image'), 'site.webmanifest')
    except TimeoutError:
        return jsonify({"status": "Timeout"}), 408
    except Exception as e:
        print(e)
        return jsonify({"status": "Unknown Error"}), 500


@app.route('/apple-touch-icon-precomposed.png')
def apple_touch_icon_precomposed():
    try:
        return send_from_directory(os.path.join(app.root_path, 'image'), 'favicon.png',
                                   mimetype='image/vnd.microsoft.icon')
    except TimeoutError:
        return jsonify({"status": "Timeout"}), 408
    except Exception as e:
        print(e)
        return jsonify({"status": "Unknown Error"}), 500
    

@app.route('/apple-touch-icon-120x120.png')
def apple_touch_icon_120x120():
    try:
        return send_from_directory(os.path.join(app.root_path, 'image'), 'favicon.png',
                                   mimetype='image/vnd.microsoft.icon')
    except TimeoutError:
        return jsonify({"status": "Timeout"}), 408
    except Exception as e:
        print(e)
        return jsonify({"status": "Unknown Error"}), 500


@app.route("/api/v1/healthcheck", methods=["GET"])
def healthcheck():
    try:
        return jsonify({"Health": "Alive"})
    except TimeoutError:
        return jsonify({"Health": "Error"}), 408
    except Exception as e:
        print(e)
        return jsonify({"Health": "Error"}), 500


@app.route("/test", methods=["GET"])
def test():
    logger.log(level="info", handler="test", content={"event": "test"})
    logger.log(level="error", handler="test", content={"event": "test"})
    logger.log(level="warning", handler="test", content={"event": "test"})
    logger.log(level="debug", handler="test", content={"event": "test"})
    logger.log(level="boot", handler="test", content={"event": "test"})
    webhook_handler.discord(title="test", description="test", color="7932020")
    return jsonify({"status": "OK"})
