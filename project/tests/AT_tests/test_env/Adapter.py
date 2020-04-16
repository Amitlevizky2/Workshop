from project.service_layer.PurchaseManager import PurchaseManager
from project.service_layer.StoresManagerInterface import StoresManagerInterface
from project.service_layer.UsersManagerInterface import UsersManagerInterface


class Adapter:
    def __init__(self):
        self.users_manager_interface = UsersManagerInterface()
        self.store_manager_interface = StoresManagerInterface(self.users_manager_interface)
        self.purchase_manager = PurchaseManager(self.users_manager_interface, self.store_manager_interface)
        self.username = self.users_manager_interface.add_guest_user()

    def register(self, username, password):
        return self.users_manager_interface.register(self.username, username, password)

    def login(self, username, password):
        return self.users_manager_interface.login(self.username, username, password)

    def showProductStore(self, store):
        pass

    def add_product_to_Store(self, store_id, product_name: str, product_price: int,
                             product_categories: [str],
                             key_words: [str], amount):
        self.store_manager_interface.add_product_to_store(store_id, self.username, product_name, product_price,
                                                          product_categories, key_words, amount)

    def searchProduct(self, product="", category=[], key_words=[]):
        self.store_manager_interface.search_product(product, category, key_words)

    def Open_store(self, store_name):
        self.store_manager_interface.open_store(self.username, store_name)

    def get_managed_stores(self):
        self.users_manager_interface.get_managed_stores(self.username)

    def logout(self):
        self.username = self.users_manager_interface.logout(self.username)
        return self.username

    def get_purchase_history(self):
        return self.users_manager_interface.view_purchases(self.username)

    def add_product(self, store_id, product, amount):
        return self.users_manager_interface.add_product(self.username,store_id,product,amount)

    def buy(self):
        return self.purchase_manager.buy(self.username)

    def remove_product_from_store(self, store_id, product_name):
        return self.store_manager_interface.re

    def update_product(self, store_id, product_name, att, updated):
        pass

    def add_new_store_owner(self, user, store_id):
        pass

    def add_permission(self, store_id, user, permission):
        pass

    def remove_store_manager(self, store_id, user):
        pass

    def view_store_history(self, store_id):
        pass
