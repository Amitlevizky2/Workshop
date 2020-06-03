import os
import json
import jsonpickle
from eventlet import wsgi
from flask import Flask, jsonify, request, current_app
from flask_socketio import SocketIO, join_room, leave_room
from flask_cors import CORS

from project.service_layer.Initializer import Initializer

import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
CORS(app)
app.secret_key = os.environ.get('SECRET')
app.config['WTF_CSRF_SECRET_KEY'] = "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"
sio = SocketIO(app, logger=True, engineio_logger=True,
               cors_allowed_origins='*', async_mode='eventlet')
# current_app(app)
with app.app_context():
    # within this block, current_app points to app.
    print("current: "+current_app.name)
    initializer = Initializer(sio)
users_manager = initializer.get_users_manager_interface()
stores_manager = initializer.get_stores_manager_interface()

"""---------------------------------------------------------------------"""
"""-------------------------------USER EVENTS-------------------------------- """
"""---------------------------------------------------------------------"""


@app.route('/guest_user_name', methods=['POST', 'GET'])
def guest_user_name():
    guest_username = users_manager.add_guest_user()
    return jsonify(
        {'guest_username': guest_username}
    )


# username: str, login_username: str, password
@app.route('/login', methods=['POST', 'GET'])
def login():
    message = request.get_json()
    print(message['username'])
    logged_in, data = users_manager.login(message['username'], message['new_username'], message['password'])
    print(data)
    response = {}
    data['error'] = not logged_in
    print(data)
    return jsonify(data)
    # if logged_in is True:
    #
    #
    #     return jsonify(data), 201
    # else:
    #     return jsonify(data), 500


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    message = request.get_json()
    answer, data = users_manager.logout(message['username'])
    data['error'] = not answer
    return jsonify(data)


@app.route('/register', methods=['POST', 'GET'])
def register():
    message = request.get_json()
    answer, data = users_manager.register(message['username'], message['new_username'], message['password'])
    data['error'] = not answer
    return jsonify(data)


@app.route('/is_manager', methods=['POST', 'GET'])
def is_manager():
    message = request.get_json()
    answer, data = users_manager.is_store_manager(message['username'])
    data['error'] = not answer
    return jsonify(data)


@app.route('/add_product', methods=['POST', 'GET'])
def add_product():
    """
    adds a product to the user's ('username') shopping cart
    :return:
    """
    message = request.get_json()
    answer, data = users_manager.add_product(message['username'], message['store_id'], message['product_name'],
                                             message['quantity'])
    data['error'] = not answer
    return jsonify(data)


@app.route('/remove_product', methods=['POST', 'GET'])
def remove_product():
    """
    removes a product from the user's ('username') shopping cart
    :return:
    """
    message = request.get_json()
    answer, data = users_manager.remove_product(message['username'], message['store_id'], message['product_name'],
                                                message['quantity'])
    data['error'] = not answer
    return jsonify(data)


@app.route('/get_cart', methods=['POST', 'GET'])
def get_cart():
    message = request.get_json()
    answer, data = jsonpickle.decode(users_manager.get_cart(message['username']))
    data['error'] = not answer
    return jsonify(data)


# TODO: implement
@app.route('/remove_cart', methods=['POST', 'GET'])
def remove_cart():
    pass


# TODO: implement
@app.route('/view_cart', methods=['POST', 'GET'])
def view_cart():
    pass


# TODO: implement
@app.route('/remove_managed_store', methods=['POST', 'GET'])
def remove_managed_store():
    pass


@app.route('/get_managed_stores', methods=['POST', 'GET'])
def get_managed_stores():
    message = request.get_json()
    answer, data = users_manager.get_managed_stores(message['username'])
    data['error'] = not answer
    return jsonify(data)


@app.route('/view_user_purchases', methods=['POST', 'GET'])
def view_user_purchases():
    message = request.get_json()
    answer, data = users_manager.view_purchases(message['username'])
    data['error'] = not answer
    return jsonify(data)


# TODO: implement
@app.route('/add_purchase', methods=['POST', 'GET'])
def add_purchase():
    pass


"""---------------------------------------------------------------------"""
"""-------------------------------STORE EVENTS------------------------------"""
"""---------------------------------------------------------------------"""


@app.route('/appoint_store_manager', methods=['POST', 'GET'])
def appoint_store_manager():
    message = request.get_json()
    answer = stores_manager.appoint_manager_to_store(message['store_id'], message['owner'], message['to_appoint'])
    if answer is True:
        return 'done', 201
    return 'error', 400


@app.route('/get_store_managers', methods=['POST', 'GET'])
def get_store_managers():
    message = request.get_json()
    answer = stores_manager.get_store_managers(message['store_id'])
    return jsonify({
        'managers': answer
    })


@app.route('/get_store_owners', methods=['POST', 'GET'])
def get_store_owners():
    message = request.get_json()
    answer = stores_manager.get_store_owners(message['store_id'])
    return jsonify({
        'owners': answer
    })


@app.route('/open_store', methods=['POST', 'GET'])
def open_store():
    message = request.get_json()
    print(message)
    answer = stores_manager.open_store(message['username'], message['store_name'])
    print('store_id: ' + str(answer))
    return jsonify({
        'data': answer
    })


@app.route('/appoint_store_owner', methods=['POST', 'GET'])
def appoint_store_owner():
    message = request.get_json()
    answer = stores_manager.appoint_owner_to_store(message['store_id'], message['owner'], message['to_appoint'])
    if answer is False:
        return 'error', 400
    return 'done', 201


@app.route('/search', methods=['POST', 'GET'])
def search():
    message = request.get_json()
    answer = jsonpickle.decode(stores_manager.search_product(message['product_name']))
    return jsonify({
        "search_results": answer
    })


@app.route('/update_store_product', methods=['POST', 'GET'])
def update_store_product():
    message = request.get_json()
    answer = stores_manager.update_product(message['store_id'], message['username'], message['product_name'],
                                           message['attribute'], message['updated'])
    if answer is True:
        return 'done', 200
    return 'error', 400


"""---------------------------------------------------------------------"""
"""-------------------------------ADMIN EVENTS------------------------------"""
"""---------------------------------------------------------------------"""


# TODO: implement
@app.route('/is_admin', methods=['POST', 'GET'])
def is_admin():
    pass


# TODO: implement
@app.route('/view_purchases_admin', methods=['POST', 'GET'])
def view_purchases_admin():
    pass


"""---------------------------------------------------------------------"""
"""-------------------------------SOCKET EVENTS------------------------------"""
"""---------------------------------------------------------------------"""


@sio.on('join')
def join(data):
    join_room(room=data['room'])


@sio.on('leave')
def leave(data):
    leave_room(room=data['room'])


def send_notification(username, message):
    str_msg = jsonpickle.decode(message)
    sio.send(jsonify({
        'messages': str_msg
    }), json=True, room=username)


"""---------------------------------------------------------------------"""
"""-------------------------------RUN APPLICATION------------------------------"""
"""---------------------------------------------------------------------"""

if __name__ == "__main__":
    wsgi.server(eventlet.listen(('', 5000)), app)
    # app.run(debug=True)
