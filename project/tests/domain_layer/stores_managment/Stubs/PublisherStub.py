from socket import SocketIO

from project.domain_layer.communication_managment.Publisher import Publisher
from project.domain_layer.users_managment.UsersManager import UsersManager


class PublisherStub(Publisher):

    def set_users_manager(self, users_manager: UsersManager):
        return True



    def send_notification(self, username, message, event):
        return True

    def store_status_update(self, store_id, store_name, users: [str], status=''):
        return True

    def store_ownership_update(self, store_id, store_name, users: [str]):
        return True

    def purchase_update(self, store_id, store_name, users: [str]):
        return True

    def notify_admins(self, statistics):
        return True

    def bound_publisher_and_stats(self):
        return True
    def store_management_update(self,store_id, store_name, users: [str], update_type=''):
        pass


    def notify(self,message,user):
        return True