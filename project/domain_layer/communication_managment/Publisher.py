from socket import SocketIO

import jsons
from flask import jsonify
from flask_socketio import emit
from jsonpickle import json

from project.domain_layer.users_managment.UsersManager import UsersManager


class Publisher:
    def __init__(self, sio: SocketIO):
        self.users_manager = None
        self.sio = sio

    def set_users_manager(self, users_manager: UsersManager):
        self.users_manager = users_manager
        self.bound_publisher_and_stats()

    def notify(self, message, user):
        print('publisher message: ' + message)
        if self.users_manager.check_if_loggedin(user):
            msg = {
                'messages': [message]
            }
            self.send_notification(user, msg, 'send')
        else:
            self.users_manager.add_notification(user, message)

    def send_notification(self, username, message, event):
        if event == 'send':
            self.sio.send(data=message, room=username)
        if event == 'statistics_update':
            print(message)
            self.sio.emit('statistics', message, room=username)

    def store_status_update(self, store_id, store_name, users: [str], status=''):
        """
       send "store closes/reopens" event notification message
        :param status: open/close.
        :param store_id:
        :param store_name:
        :param users: list of recipients (user names)
        :return:
        """
        open_message = "Dear {}, " \
                       'we are glad to inform your store: {} is now open!'
        close_message = 'Dear {}, ' \
                        'your store: {} has been closed.'
        for owner in users:
            if status == 'open':
                message = open_message
            else:
                message = close_message
            notification = message.format(owner, store_name)
            self.notify(notification, owner)

    # store owner get notification when their appointment as store owner was removed
    def store_ownership_update(self, store_id, store_name, users: [str], update_type=''):
        """
        send "store owner appointment" event notification message
        :param update_type:
        :param status: add permissions or removed permissions
        :param store_id:
        :param store_name:
        :param users: list of recipients (user names)
        :return:
        """
        appointment_message = 'Dear {}, ' \
                              'you are appointed as a store owner, of store: {}.'
        message = 'Dear {}, ' \
                  'your store owner appointment of store: {} was removed and is no longer valid.'
        if update_type == 'appoint':
            message = appointment_message
        for owner in users:
            notification = message.format(owner, store_name)
            self.notify(notification, owner)

    def store_management_update(self, store_id, store_name, users: [str], update_type=''):
        """
        send "store owner appointment" event notification message
        :param update_type:
        :param status: add permissions or removed permissions
        :param store_id:
        :param store_name:
        :param users: list of recipients (user names)
        :return:
        """
        appointment_message = 'Dear {}, ' \
                              'you are appointed as a store manager, of store: {}.'
        changed_message = 'Dear {}, ' \
                          'your permissions as store manager of store: {}, where changed.'
        message = 'Dear {}, ' \
                  'your store manager appointment of store: {} was removed and is no longer valid.'
        if update_type == 'appoint':
            message = appointment_message
        if update_type == 'changed':
            message = changed_message
        for owner in users:
            notification = message.format(owner, store_name)
            self.notify(notification, owner)

    # store owner get notification when a client buys a product from the store
    def purchase_update(self, store_id, store_name, users: [str]):
        """
        send "new purchase" event notification message
        :param store_id:
        :param store_name:
        :param users: list of recipients (user names)
        :return:
        """
        message = 'Dear {}, ' \
                  'We are glad to inform that an item from your store: {} has been purchased. ' \
                  'For more information, please check out purchase history.'
        for owner in users:
            notification = message.format(owner, store_name)
            self.notify(notification, owner)

    def notify_admins(self, statistics):
        self.send_notification('admins', statistics, 'statistics_update')

    def bound_publisher_and_stats(self):
        self.users_manager.bound_publisher_and_stats(self)
