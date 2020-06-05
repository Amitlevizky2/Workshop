from socket import SocketIO

from flask import jsonify
from jsonpickle import json

from project.domain_layer.users_managment.UsersManager import UsersManager


class Publisher:
    def __init__(self, sio: SocketIO):
        self.users_manager = None
        self.sio = sio

    def set_users_manager(self, users_manager: UsersManager):
        self.users_manager = users_manager

    def notify(self, message, user):
        print('publisher message: ' + message)
        if self.users_manager.check_if_loggedin(user):
            self.send_notification(user, message)
        else:
            self.users_manager.add_notification(user, message)

    def send_notification(self, username, message):
        self.sio.send({
            'messages': message
        }, json=True, room=username)

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
    def store_ownership_update(self, store_id, store_name, users: [str]):
        """
        send "store owner appointment" event notification message
        :param store_id:
        :param store_name:
        :param users: list of recipients (user names)
        :return:
        """
        message = 'Dear {}, ' \
                  'your store owner appointment of store: {} was removed and is no longer valid.'
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
