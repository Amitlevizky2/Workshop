import os
import json
import jsonpickle
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, join_room, leave_room
from flask_cors import CORS

from project.service_layer.Initializer import Initializer

app = Flask(__name__)
CORS(app)
app.secret_key = os.environ.get('SECRET')
app.config['WTF_CSRF_SECRET_KEY'] = "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"
sio = SocketIO(app, manage_session=False)

initializer = Initializer()
users_manager = initializer.get_users_manager_interface()
stores_manager = initializer.get_stores_manager_interface()


@app.route('/guest_user_name', methods=['POST', 'GET'])
def guest_user_name():
    guest_username = users_manager.add_guest_user()
    return jsonify({
        'username': guest_username
    })


# username: str, login_username: str, password
@app.route('/login', methods=['POST'])
def login():
    message = request.get_json()
    answer = users_manager.login(message['username'], message['new_username'], message['password'])
    if answer is False:
        return 'error', 400
    return jsonify({
        'user': answer
    }), 201


@app.route('/logout', methods=['POST'])
def logout():
    message = request.get_json()
    answer = users_manager.logout(message['username'])
    logged_out = True
    # if user is not logged out --> still logged in
    if not answer == message['username']:
        logged_out = False
    return json.dumps({
        'logged_out': logged_out,
        'username': answer
    })


@app.route('/register', methods=['POST'])
def register():
    message = request.get_json()
    answer = users_manager.register(message['username'], message['new_username'], message['password'])
    return jsonify({
        'registered': answer
    })


@app.route('/is_manager', methods=['POST'])
def is_manager():
    message = request.get_json()
    answer = users_manager.is_store_manager(message['username'])
    return jsonify({
        'manager': answer
    })


@app.route('/add_product', methods=['POST'])
def add_product():
    message = request.get_json()
    answer = users_manager.add_product(message['username'], message['store_id'], message['product_name'],
                                       message['quantity'])
    if answer is True:
        return 'done', 201
    return 'error', 400


@app.route('/remove_product', methods=['POST'])
def remove_product():
    message = request.get_json()
    answer = users_manager.remove_product(message['username'], message['store_id'], message['product_name'],
                                          message['quantity'])
    if answer is True:
        return 'removed', 201
    return 'error', 400


@app.route('/get_cart', methods=['POST'])
def get_cart():
    message = request.get_json()
    answer = jsonpickle.decode(users_manager.get_cart(message['username']))
    return jsonify({
        'cart': answer
    })


# TODO: implement
@app.route('/remove_cart', methods=['POST'])
def remove_cart():
    pass


# TODO: implement
@app.route('/view_cart', methods=['POST'])
def view_cart():
    pass


@app.route('/add_managed_store', methods=['POST'])
def add_managed_store():
    message = request.get_json()
    answer = users_manager.add_managed_store(message['username'], message['store_id'])
    if answer is True:
        return 'done', 201
    return 'error', 400


# TODO: implement
@app.route('/remove_managed_store', methods=['POST'])
def remove_managed_store():
    pass


@app.route('/get_managed_stores', methods=['POST'])
def get_managed_stores():
    message = request.get_json()
    answer = users_manager.get_managed_stores(message['username'])
    return jsonify({
        'managed_stores': answer
    })


@app.route('/open_store', methods=['POST'])
def open_store():
    message = request.get_json()
    answer = stores_manager.open_store(message['username'], message['store_name'])
    return jsonify({
        'store_id': answer
    })


@app.route('/search', methods=['POST'])
def search():
    message = request.get_json()
    answer = jsonpickle.decode(stores_manager.search_product(message['product_name']))
    return jsonify({
        "search_results": answer
    })


@app.route('/view_user_purchases', methods=['POST'])
def view_user_purchases():
    message = request.get_json()
    answer = jsonpickle.decode(users_manager.view_purchases(message['username']))
    return jsonify({
        "purchase_history": answer
    })


# TODO: implement
@app.route('/add_purchase', methods=['POST'])
def add_purchase():
    pass


# TODO: implement
@app.route('/is_admin', methods=['POST'])
def is_admin():
    pass


# TODO: implement
@app.route('/view_purchases_admin', methods=['POST'])
def view_purchases_admin():
    pass


@sio.on('create_room')
def create_room(sid, username):
    join_room(room=username, sid=sid)


@sio.on('exit_room')
def exit_room(sid, username):
    leave_room(room=username, sid=sid)


def send_notification(username, message):
    str_msg = jsonpickle.decode(message)
    sio.send(jsonify({
        'message': str_msg
    }), json=True, room=username)


if __name__ == "__main__":
    app.run(debug=True)

    """
if __name__ == '__main__':
    

      wsgi.server(eventlet.wrap_ssl(eventlet.listen(('', 5000)),
                                      certfile='cert.crt',
                                      keyfile='private.key',
                                      server_side=True),
                    app)

      
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)    
    """

"""
def exchange_username(old_username, new_username, sid):
    clients.pop(old_username)
    sio.close_room(old_username)
    clients[new_username] = sid
    create_room(sid, new_username)
    session = sio.get_session(sid)
    session['username'] = new_username
"""
