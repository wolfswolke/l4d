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
