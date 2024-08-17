from flask_definitions import *

@app.route('/logging', methods=['GET'])
def logging():
    if 'session' in request.cookies:
        user_id = session_manager.get_user_id(request.cookies['session'])
        if user_id is None:
            response = redirect(url_for('profile'))
            response.set_cookie('session', value='', expires=0)
            return response
        data = mongo.get_data_with_list(user_id, ["token", "username"], mongo_collection)
        if data is None:
            session_manager.remove_session(request.cookies['session'])
            response = redirect(url_for('profile'))
            response.set_cookie('session', value='', expires=0)
            return response
        return render_template('logging.html', user_name=data['username'])
    else:
        return redirect(url_for('profile'))

@app.route('/api/v1/get_logs', methods=['GET'])
def get_logs():
    if 'session' in request.cookies:
        user_id = session_manager.get_user_id(request.cookies['session'])
        if user_id is None:
            return jsonify({"status": "error", "message": "Invalid Session"}), 401
        data = mongo.get_data_with_list(user_id, ["token", "username"], mongo_collection)
        if data is None:
            session_manager.remove_session(request.cookies['session'])
            return jsonify({"status": "error", "message": "Invalid Session"}), 401
        fluent_logs = mongo.get_logs("fluent")
        fluent_logs_clean = []
        for log in fluent_logs:
            log.pop("_id")
            fluent_logs_clean.append(log)
        firehose_logs = mongo.get_logs("firehose")
        print(fluent_logs, firehose_logs)
        return jsonify({"fluent": fluent_logs_clean, "firehose": firehose_logs})
    else:
        return jsonify({"status": "error", "message": "Invalid Session"}), 401