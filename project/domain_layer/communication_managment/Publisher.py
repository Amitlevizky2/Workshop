from project.domain_layer.users_managment.UsersManager import UsersManager


class Publisher:
    def __init__(self):
        self.users_manager = None

    def set_users_manager(self, users_manager: UsersManager):
        self.users_manager = users_manager

    def notify(self, message, user):
        from project.service_layer.communication.Gateway import send_notification
        if self.users_manager.check_if_loggedin(user):
            send_notification(user, message)
        else:
            self.users_manager.add_notification(user, message)

    def store_status_update(self, store_id, store_name,  users: [str]):
        """
       send "store closes/reopens" event notification message
        :param store_id:
        :param store_name:
        :param users: list of recipients (user names)
        :return:
        """
        pass

# store owner get notification when their appointment as store owner was removed
    def store_ownership_update(self, store_id, store_name, users: [str]):
        """
        send "store owner appointment" event notification message
        :param store_id:
        :param store_name:
        :param users: list of recipients (user names)
        :return:
        """
        pass

# store owner get notification when a client buys a product from the store
    def purchase_update(self, store_id, store_name, users: [str]):
        """
        send "new purchase" event notification message
        :param store_id:
        :param store_name:
        :param users: list of recipients (user names)
        :return:
        """
        # message = 'Dear %s,' \
        #           'We are glad to announce that your store:' \
        #           'store name: %s  '
        pass




