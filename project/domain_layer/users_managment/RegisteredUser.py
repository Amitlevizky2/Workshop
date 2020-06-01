import jsons

from project.domain_layer.users_managment.User import User


class RegisteredUser(User):

    def __init__(self, username):
        super().__init__(username)
        self.username = username
        self.purchase_history = []
        self.loggedin = False
        self.managed_stores = []
        self.notifications = []

    def logout(self):
        self.loggedin = False

    def login(self):
        self.loggedin = True

    def view_purchase_history(self, view_format=''):
        """
        :param view_format: enter 'json' to get json format
        :return: list of user's purchases or list of user's json purchases
        """
        if view_format == 'json':
            return self.get_jsn_purchase_history()
        return self.purchase_history

    def get_managed_store(self):
        return self.managed_stores

    def add_managed_store(self, store_id) -> bool:
        """
        :param store_id:
        :return: if store_id is in managed_stores return False. Otherwise, add store_id and return True
        """
        if store_id not in self.managed_stores:
            self.managed_stores.append(store_id)
            return True
        return False

    def remove_managed_store(self, store_id):
        """
        :param store_id:
        :return: if store_id is in managed_stores, remove and return True. Otherwise, return False
        """
        if store_id in self.managed_stores:
            self.managed_stores.remove(store_id)
            return True, 'Store id: ' + store_id + ' is not managed by ' + self.username + ' anymore.'
        return False, 'Store id: ' + store_id + ' is not associated with the user:  ' + self.username + '.'

    def add_notification(self, message):
        self.notifications.append(message)

    def have_notifications(self) -> bool:
        return self.notifications.__len__() > 0

    def clear_notifications(self):
        self.notifications.clear()

    def get_notifications(self):
        messages = self.notifications
        # self.notifications.clear()
        return messages

    def is_store_manager(self):
        return self.managed_stores.__len__() > 0

    def get_jsn_description(self):
        json_cart = self.cart.get_jsn_description()
        json_purchase_history = self.get_jsn_purchase_history()
        json_managed_stores = self.get_json_managed_stores()
        json_notifications = self.get_json_notifications()
        return jsons.dumps({
            'username': self.username,
            'cart': json_cart,
            'purchase_history': json_purchase_history,
            'managed_stores': json_managed_stores,
            'notifications': json_notifications
        })

    def get_jsn_purchase_history(self):
        return []

    def get_json_managed_stores(self):
        managed_stores = []
        for store_id in self.managed_stores:
            managed_stores.append({
                'store_id': store_id
            })
        return managed_stores

    def get_json_notifications(self):
        notifications = []
        for message in self.notifications:
            notifications.append({
                'message': message
            })
        return notifications
