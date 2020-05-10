from project.domain_layer.users_managment.UsersManager import UsersManager


class Publisher:
    def __init__(self):
        self.users_manager = None

    def set_users_manager(self, users_manager: UsersManager):
        self.users_manager = users_manager

    def purchased_items_update(self, message, users: [str]):
        from project.service_layer.communication.Gateway import send_notification
        for user in users:
            if self.users_manager.check_if_loggedin(user):
                send_notification(user, message)
            else:
                self.users_manager.add_notification(user, message)





