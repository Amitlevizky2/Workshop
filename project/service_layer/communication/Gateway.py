import eventlet
from eventlet import wsgi
import socketio
import json
import jsonpickle

from project.service_layer.Initializer import Initializer

sio = socketio.Server(async_handlers=False)
initializer = Initializer()
users_manager = initializer.get_users_manager_interface()
stores_manager = initializer.get_stores_manager_interface()
# purchase_manager = PurchaseManager(users_manager, stores_manager)

# clients = { username, sid? }
clients = {}
app = socketio.WSGIApp(sio)

"""
on connect:
1. assign the user with a new guest user name.
2. save session?
3. save session-guest user name
4. create a room
"""


@sio.on('start')
def establish_connection(sid, message):
    guest_username = users_manager.add_guest_user()
    print('user name: ' + guest_username)
    clients[guest_username] = sid
    sio.save_session(sid, {'username': guest_username})
    create_room(sid, guest_username)
    return json.dumps({
        'username': guest_username
    })


@sio.on('disconnect')
def disconnect(sid):
    session = sio.get_session(sid)
    username = session['username']
    sio.emit('disconnect', room=username)
    clients.pop(session['username'])
    # print('disconnect ', sid)


@sio.on('create room')
def create_room(sid, username):
    sio.enter_room(sid, room=username)


@sio.on('exit room')
def exit_room(sid, username):
    sio.leave_room(sid, room=username)


# username: str, login_username: str, password
@sio.on('login')
def login(sid, message):
    json_msg = get_json_obj(message)
    answer = users_manager.login(json_msg['username'], json_msg['login_username'], json_msg['password'])
    if answer is True:
        exchange_username(json_msg['username'], answer, sid)
    return json.dumps({
        'loggedin': answer
    })


@sio.on('logout')
def logout(sid, message):
    json_msg = get_json_obj(message)
    answer = users_manager.logout(json_msg['username'])
    if not answer == json_msg['username']:
        exchange_username(json_msg['username'], answer, sid)
    return json.dumps({
        'username': answer
    })


@sio.on('register')
def register(sid, message):
    json_msg = get_json_obj(message)
    answer = users_manager.register(json_msg['username'], json_msg['new_username'], json_msg['password'])
    if answer is True:
        exchange_username(json_msg['username'], json_msg['new_username'], sid)
    return json.dumps({
        'registered': answer
    })


@sio.on('is manager')
def is_manager(sid, message):
    json_msg = get_json_obj(message)
    answer = users_manager.is_store_manager(json_msg['username'])
    return json.dumps({
        'manager': answer
    })


@sio.on('add product')
def add_product(sid, message):
    json_msg = get_json_obj(message)
    answer = users_manager.add_product(json_msg['username'], json_msg['store_id'], json_msg['product_name'],
                                       json_msg['quantity'])
    # return something?


@sio.on('get cart')
def get_cart(sid, message):
    json_msg = get_json_obj(message)
    answer = users_manager.get_cart(json_msg['username'])
    return answer


@sio.on('open store')
def open_store(sid, message):
    json_msg = get_json_obj(message)
    answer = stores_manager.open_store(json_msg['username'], json_msg['store_name'])
    return json.dumps({
        'store_id': answer
    })


@sio.on('search')
def search(sid, message):
    json_msg = get_json_obj(message)
    answer = stores_manager.search_product(json_msg['product_name'])
    return answer


def exchange_username(old_username, new_username, sid):
    clients.pop(old_username)
    sio.close_room(old_username)
    clients[new_username] = sid
    create_room(sid, new_username)
    session = sio.get_session(sid)
    session['username'] = new_username


def send_notification(username, message):
    str_msg = jsonpickle.decode(message)
    sio.emit('notification', json.dumps({
        'message': str_msg
    }), room=clients[username])


def get_json_obj(message):
    return json.loads(message)


if __name__ == '__main__':
    """

      wsgi.server(eventlet.wrap_ssl(eventlet.listen(('', 5000)),
                                      certfile='cert.crt',
                                      keyfile='private.key',
                                      server_side=True),
                    app)

      """
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
