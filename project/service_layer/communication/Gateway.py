import os
import json
import jsonpickle
import jsons
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
clients = {}
# current_app(app)
with app.app_context():
    # within this block, current_app points to app.
    print("current: " + current_app.name)
    initializer = Initializer(sio)
users_manager = initializer.get_users_manager_interface()
stores_manager = initializer.get_stores_manager_interface()
purchase_manager = initializer.get_purchase_manager_interface()

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
    answer = users_manager.login(message['username'], message['new_username'], message['password'])
    print(answer)
    return jsonify(answer)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    message = request.get_json()
    answer = users_manager.logout(message['username'])
    return answer


@app.route('/register', methods=['POST', 'GET'])
def register():
    message = request.get_json()
    data = users_manager.register(message['username'], message['new_username'], message['password'])
    return data


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
    print(message)
    data = users_manager.add_product(message['username'], message['store_id'], message['product_name'],
                                     message['quantity'])
    return jsonify(data)


@app.route('/remove_product', methods=['POST', 'GET'])
def remove_product():
    """
    removes a product from the user's ('username') shopping cart
    :return:
    """
    message = request.get_json()
    data = users_manager.remove_product(message['username'], message['store_id'], message['product_name'],
                                                message['quantity'])
    return data


@app.route('/get_cart', methods=['POST', 'GET'])
def get_cart():
    message = request.get_json()
    answer, data = jsonpickle.decode(users_manager.get_cart(message['username']))
    data['error'] = not answer
    return jsonify(data)


@app.route('/view_cart', methods=['POST', 'GET'])
def view_cart():
    message = request.get_json()
    answer = users_manager.view_cart(message['username'])
    return jsonify(answer)


@app.route('/get_managed_stores', methods=['POST', 'GET'])
def get_managed_stores():
    message = request.get_json()
    data = users_manager.get_managed_stores_description(message['username'])
    return jsonify(data)


@app.route('/view_user_purchases', methods=['POST', 'GET'])
def view_user_purchases():
    message = request.get_json()
    print(message)
    if message['is_admin'] is True:
        answer = users_manager.view_purchases_admin(message['username'], message['admin'])
        print(answer)
        return answer
    data = users_manager.view_purchases(message['username'])
    print(data)
    return data


@app.route('/buy', methods=['POST', 'GET'])
def buy():
    message = request.get_json()
    data = purchase_manager.buy(message['username'], message['number'], message['month'], message['year'],
                                message['holder'], message['ccv'], message['id'], message['address'], message['city'],
                                message['country'], message['zip'])
    return jsonify(data)


"""---------------------------------------------------------------------"""
"""-------------------------------STORE EVENTS------------------------------"""
"""---------------------------------------------------------------------"""


@app.route('/appoint_store_manager', methods=['POST', 'GET'])
def appoint_store_manager():
    message = request.get_json()
    answer = stores_manager.appoint_manager_to_store(message['store_id'], message['owner'], message['to_appoint'])
    return jsonify(answer)


@app.route('/remove_store_manager', methods=['POST', 'GET'])
def remove_store_manager():
    message = request.get_json()
    answer = stores_manager.remove_manager(message['store_id'], message['owner'], message['to_remove'])
    return answer


@app.route('/add_product_to_store', methods=['POST', 'GET'])
def add_product_to_store():
    message = request.get_json()
    data = stores_manager.add_product_to_store(message['store_id'], message['username'], message['product_name'],
                                               message['price'], message['categories'], message['key_words'],
                                               message['amount'])
    print(data)
    return jsonify(data)


@app.route('/get_store_managers', methods=['POST', 'GET'])
def get_store_managers():
    message = request.get_json()
    answer = stores_manager.get_store_managers(message['store_id'])
    return answer


@app.route('/get_store_owners', methods=['POST', 'GET'])
def get_store_owners():
    message = request.get_json()
    answer = stores_manager.get_store_owners(message['store_id'])
    return answer


@app.route('/open_store', methods=['POST', 'GET'])
def open_store():
    message = request.get_json()
    print(message)
    answer = stores_manager.open_store(message['username'], message['store_name'])
    print('store_id: ' + str(answer))
    return jsonify({
        'error': False,
        'data': answer
    })


@app.route('/appoint_store_owner', methods=['POST', 'GET'])
def appoint_store_owner():
    message = request.get_json()
    print(message)
    answer = stores_manager.appoint_owner_to_store(message['store_id'], message['owner'], message['to_appoint'])
    print(answer)
    return jsonify(answer)


@app.route('/remove_store_owner', methods=['POST', 'GET'])
def remove_managed_store():
    message = request.get_json()
    answer = stores_manager.remove_owner(message['store_id'], message['owner'], message['to_remove'])
    return answer


@app.route('/search', methods=['POST', 'GET'])
def search():
    message = request.get_json()
    print(message)
    search_res = stores_manager.search(search_term=message['product_name'])
    print(search_res)
    answer = jsons.loads(search_res)
    return jsonify({
        'error': False,
        "data": answer
    })


@app.route('/update_store_product', methods=['POST', 'GET'])
def update_store_product():
    message = request.get_json()
    answer = stores_manager.update_product(message['store_id'], message['username'], message['product_name'],
                                           message['price'], message['amount'])
    return answer


@app.route('/remove_product_from_store', methods=['POST', 'GET'])
def remove_product_from_store():
    message = request.get_json()
    answer = stores_manager.remove_product(message['store_id'], message['product_name'], message['username'])
    return answer


@app.route('/get_stores', methods=['POST', 'GET'])
def get_stores():
    message = request.get_json()
    stores_res = stores_manager.get_stores()
    print(stores_res)
    answer = jsons.loads(stores_res)
    return jsonify({
        'error': False,
        'data': answer
    })


@app.route('/get_store_sales_history', methods=['POST', 'GET'])
def get_store_sales_history():
    """
    :return: store purchase history. username can be admin's username as well.
    """
    message = request.get_json()
    answer = stores_manager.get_sales_history(message['store_id'], message['username'])
    return jsonify(answer)


@app.route('/add_visible_discount', methods=['POST', 'GET'])
def add_visible_discount():
    message = request.get_json()
    print(message)
    answer = stores_manager.add_visible_discount_to_product(message['store_id'], message['username'],
                                                            message['start_date'], message['end_date'],
                                                            message['percent'], message['products'])
    data = jsons.loads(answer)
    return jsonify(data)


@app.route('/get_discounts', methods=['POST', 'GET'])
def get_discounts():
    message = request.get_json()
    answer = stores_manager.get_discounts(message['store_id'])
    data = jsons.loads(answer)
    print(data)
    return jsonify({
        'error': False,
        'data': data['desc']
    })


@app.route('/edit_conditional_store_discount', methods=['POST', 'GET'])
def edit_conditional_store_discount():
    message = request.get_json()
    answer = stores_manager.edit_conditional_discount_to_store(message['store_id'], message['discount_id'],
                                                               message['username'], message['start_date'],
                                                               message['end_date'], message['percent'],
                                                               message['min_price'])
    return jsonify(answer)


@app.route('/edit_conditional_product_discount', methods=['POST', 'GET'])
def edit_conditional_product_discount():
    message = request.get_json()
    answer = stores_manager.edit_conditional_discount_to_product(message['store_id'], message['discount_id'],
                                                                 message['username'], message['start_date'],
                                                                 message['end_date'], message['percent'],
                                                                 message['min_price'], message['nums_to_apply'],
                                                                 message['products'])
    return answer


@app.route('/edit_visible_product_discount', methods=['POST', 'GET'])
def edit_visible_product_discount():
    message = request.get_json()
    answer = stores_manager.edit_visible_discount_to_products(message['store_id'], message['discount_id'],
                                                              message['username'], message['start_date'],
                                                              message['end_date'], message['percent'],
                                                              message['products'])
    return answer


@app.route('/edit_store_manager_permissions', methods=['POST', 'GET'])
def edit_store_manager_permissions():
    message = request.get_json()
    answer = stores_manager.edit_store_manager_permissions(message['store_id'], message['owner'],
                                                           message['manager'], message['permissions'])
    print(answer)
    return answer


@app.route('/add_composite_discount', methods=['POST', 'GET'])
def add_composite_discount():
    message = request.get_json()
    # answer = stores_manager.add_composite_discount(message['discount'], message['products'])
    answer = stores_manager.add_composite_discount(message['store_id'], message['username'], message['start_date'],
                                                   message['end_date'], message['logic_operator'],
                                                   {message['discount']: message['products']},
                                                   [message['discounts_to_apply_id']])
    return answer


@app.route('/add_product_conditional_discount', methods=['POST', 'GET'])
def add_product_conditional_discount():
    message = request.get_json()
    answer = stores_manager.add_conditional_discount_to_product(message['store_id'], message['username'],
                                                                message['start_date'], message['end_date'],
                                                                message['percent'], message['min_amount'],
                                                                message['num_prods_to_apply'], message['products'])
    return answer


@app.route('/add_store_conditional_discount', methods=['POST', 'GET'])
def add_store_conditional_discount():
    message = request.get_json()
    answer = stores_manager.add_conditional_discount_to_store(message['store_id'], message['username'],
                                                              message['start_date'], message['end_date'],
                                                              message['percent'], message['min_price'])

    return answer


@app.route('/get_purchases_policies', methods=['POST', 'GET'])
def get_purchases_policies():
    message = request.get_json()
    answer = stores_manager.get_purchases_policies(message['store_id'])
    print(answer)
    return answer


@app.route('/get_purchase_policy_details', methods=['POST', 'GET'])
def get_purchase_policy_details():
    message = request.get_json()
    return stores_manager.get_purchase_policy_details(message['store_id'], message['purchase_policy_id'])


@app.route('/remove_product_from_discount', methods=['POST', 'GET'])
def remove_product_from_discount():
    message = request.get_json()
    return stores_manager.remove_product_from_discount(message['store_id'], message['permitted_user'],
                                                       message['discount_id'], message['product_name'])


@app.route('/get_discount_details', methods=['POST', 'GET'])
def get_discount_details():
    message = request.get_json()
    return stores_manager.get_discount_details(message['store_id'], message['discount_id'])


@app.route('/remove_product_from_purchase_product_policy', methods=['POST', 'GET'])
def remove_product_from_purchase_product_policy():
    message = request.get_json()
    answer = stores_manager.remove_product_from_purchase_product_policy(message['store_id'], message['policy_id'],
                                                                        message['permitted_user'],
                                                                        message['product_name'])
    return jsonify(answer)


@app.route('/remove_purchase_policy', methods=['POST', 'GET'])
def remove_purchase_policy():
    message = request.get_json()
    answer = stores_manager.remove_purchase_policy(message['store_id'], message['applying_username'],
                                                   message['policy_id'])

    return answer


@app.route('/add_product_to_purchase_product_policy', methods=['POST', 'GET'])
def add_product_to_purchase_product_policy():
    message = request.get_json()
    answer = stores_manager.add_product_to_purchase_product_policy(message['store_id'], message['policy_id'],
                                                                   message['permitted_user'],
                                                                   message['product_name'])
    return answer


@app.route('/add_policy_to_purchase_composite_policy', methods=['POST', 'GET'])
def add_policy_to_purchase_composite_policy():
    message = request.get_json()
    answer = stores_manager.add_policy_to_purchase_composite_policy(message['store_id'], message['applying_username'],
                                                                    message['composite_id'],
                                                                    message['policy_id'])
    return answer


@app.route('/add_purchase_composite_policy', methods=['POST', 'GET'])
def add_purchase_composite_policy():
    message = request.get_json()
    answer = stores_manager.add_purchase_composite_policy(message['store_id'], message['applying_username'],
                                                          message['purchase_policies_id'],
                                                          message['logic_operator'])
    return answer


@app.route('/add_purchase_product_policy', methods=['POST', 'GET'])
def add_purchase_product_policy():
    message = request.get_json()
    answer = stores_manager.add_purchase_product_policy(message['store_id'], message['applying_username'],
                                                        message['min_amount_products'],
                                                        message['max_amount_products'], message['products'])
    return answer


@app.route('/add_purchase_store_policy', methods=['POST', 'GET'])
def add_purchase_store_policy():
    message = request.get_json()
    answer = stores_manager.add_purchase_store_policy(message['store_id'], message['applying_username'],
                                                      message['min_amount_products'],
                                                      message['max_amount_products'])
    return answer


# TODO: the function remove_permission_from_manager_in_store in stores manager interface dose not return a value.
@app.route('/remove_store_manager_permission', methods=['POST', 'GET'])
def remove_store_manager_permission():
    message = request.get_json()
    answer = stores_manager.remove_permission_from_manager_in_store(message['store_id'], message['owner'],
                                                                    message['manager'],
                                                                    message['permission'])
    return answer


@app.route('/add_store_manager_permission', methods=['POST', 'GET'])
def add_store_manager_permission():
    message = request.get_json()
    answer = stores_manager.add_permission_to_manager_in_store(message['store_id'], message['owner'],
                                                               message['manager'],
                                                               message['permission'])
    return jsonify(answer)


@app.route('/get_user_permissions', methods=['POST', 'GET'])
def get_user_permissions():
    message = request.get_json()
    answer = stores_manager.get_user_permissions(message['store_id'], message['username'])
    print(answer)
    return answer


"""---------------------------------------------------------------------"""
"""-------------------------------ADMIN EVENTS------------------------------"""
"""---------------------------------------------------------------------"""


@app.route('/is_admin', methods=['POST', 'GET'])
def is_admin():
    message = request.get_json()
    data = users_manager.is_admin(message['username'])
    return jsonify(data)


@app.route('/view_purchases_admin', methods=['POST', 'GET'])
def view_purchases_admin():
    message = request.get_json()
    data = users_manager.view_purchases_admin(message['username'], message['admin'])
    return data


@app.route('/add_admin', methods=['POST', 'GET'])
def add_admin():
    message = request.get_json()
    data = users_manager.add_admin(message['admin'], message['future_admin'])
    return data


@app.route('/get_all_users', methods=['POST', 'GET'])
def get_all_users():
    message = request.get_json()
    data = users_manager.get_all_users(message['admin'])
    print(data)
    return data


@app.route('/get_range_statistics', methods=['POST', 'GET'])
def get_range_statistics():
    message = request.get_json()
    data = users_manager.get_range_statistics(message['start_date'], message['end_date'])
    print(data)
    return data


"""---------------------------------------------------------------------"""
"""-------------------------------SOCKET EVENTS------------------------------"""
"""---------------------------------------------------------------------"""


@sio.on('join')
def join(data):
    sid = request.sid
    clients[sid] = data['room']
    join_room(room=data['room'])


@sio.on('leave')
def leave(data):
    sid = request.sid
    clients.pop(sid)
    leave_room(room=data['room'])


@sio.on('disconnect')
def disconnect():
    sid = request.sid
    if sid in clients.keys():
        username = clients[sid]
        guest_username = users_manager.logout(username)
        clients.pop(sid)
        leave_room(room=username)
        print('user {} is logged out!'.format(username))
    leave_room(room=sid)


@sio.on('get_today_stats', namespace='/statistics')
def get_today_stats():
    today_stats = users_manager.get_today_stats()
    # sio.emit('today_stats', )
    # print('received json: ' + str(json))


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
