from project.domain_layer.communication_managment.Publisher import Publisher
from project.service_layer.StoresManagerInterface import StoresManagerInterface
from project.service_layer.UsersManagerInterface import UsersManagerInterface


class Initializer:
    def __init__(self):
        self.users_manager = UsersManagerInterface()
        self.stores_manager = StoresManagerInterface(self.users_manager)
        self.publisher = Publisher()
        self.users_manager.set_stores_manager(self.stores_manager)
        self.stores_manager.bound_publisher(self.publisher)

    def get_users_manager_interface(self) -> UsersManagerInterface:
        return self.users_manager

    def get_stores_manager_interface(self) -> StoresManagerInterface:
        return self.stores_manager

    def bound_managers(self):
        users = self.users_manager.get_users_manager()
        stores = self.stores_manager.get_stores_manager()
        users.set_stores_manager(stores)
        stores.set_users_manager(users)
