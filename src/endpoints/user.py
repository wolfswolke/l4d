from flask_definitions import *


@app.route('/user', methods=['GET'])
def profile():
    if 'session' in request.cookies:
        user_id = session_manager.get_user_id(request.cookies['session'])
        if user_id is None:
            response = redirect(url_for('user'))
            response.set_cookie('session', value='', expires=0)
            return response
        data = mongo.get_data_with_list(user_id, ["token", "username"], mongo_collection)
        if data is None:
            session_manager.remove_session(request.cookies['session'])
            response = redirect(url_for('user'))
            response.set_cookie('session', value='', expires=0)
            return response
        user_data = {
            'user_id': user_id,
            'token': data['token'],
            'username': data['username']
        }
        return render_template('user.html', user_data=user_data)
    else:
        return render_template('login.html')


@app.route('/api/v1/user_handling/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data['username']
        password = data['password']
        ret_val = mongo.user_handling(username, password, register=True)
        if ret_val is None:
            return jsonify({"status": "error","message": "Internal Server Error"}), 500
        elif ret_val["status"] == "ERROR":
            return jsonify({"status": "error","message": ret_val["message"]}), 400
        else:
            session_id = session_manager.create_session(ret_val['user_id'])
            response = jsonify({"status": "OK"})
            response.set_cookie('session', value=session_id)
            return response, 200
    except KeyError:
        return jsonify({"status": "error","message": "Missing username or password"}), 400
    except Exception as e:
        logger.log(level="error", handler="user", content={"event": "login", "error": str(e)})
        return jsonify({"status": "error","message": "Internal Server Error"}), 500


@app.route('/api/v1/user_handling/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data['username']
        password = data['password']
        ret_val = mongo.user_handling(username, password, register=False)
        if ret_val is None:
            return jsonify({"error": "Internal Server Error"}), 500
        elif ret_val["status"] == "ERROR":
            return jsonify(ret_val), 400
        else:
            response = jsonify(ret_val)
            session_id = session_manager.create_session(ret_val['user_id'])
            response.set_cookie('session', value=session_id)
            return response, 200
    except KeyError:
        return jsonify({"error": "Missing username or password"}), 400
    except Exception as e:
        logger.log(level="error", handler="user", content={"event": "login", "error": str(e)})
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/api/v1/user_handling/logout', methods=['POST'])
def logout():
    session_manager.remove_session(request.cookies['session'])
    response = jsonify({"status": "ok"})
    response.set_cookie('session', value='', expires=0)
    return response, 200