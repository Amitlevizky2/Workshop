from project.domain_layer.users_managment.Cart import Cart
from project.domain_layer.users_managment.UsersManager import UsersManager
from project import logger
from project.service_layer.Security import Security
from project.service_layer.StoresManagerInterface import StoresManagerInterface


class UsersManagerInterface:
    security = Security()

    def __init__(self):
        self.user_manager = UsersManager()
        self.stores_manager = None
        username = self.user_manager.add_guest_user()
        self.user_manager.register(username, "admin")
        self.user_manager.admins.append("admin")

    def set_stores_manager(self, stores_manager: StoresManagerInterface):
        self.stores_manager = stores_manager

    def register(self, username, new_username, password):
        logger.log("user %s called register with new_username:%s", username, new_username)
        if self.user_manager.register(username, new_username):
            self.security.add_user(new_username, password)
            return True
        else:
            return False

    # EVERYTIME SOMEONE OPENS THE SYSTEM A NEW USER IS CREATEDDDDDDDD
    def login(self, username: str, login_username: str, password) -> bool:
        logger.log("user %s called login with login_username:%s", username, login_username)
        if self.security.verify_password(login_username, password):
            return self.user_manager.login(username, login_username)
        else:
            return False

    def add_guest_user(self):
        return self.user_manager.add_guest_user()

    # look up via usr id change user list to map of ids and user
    def view_cart(self, username) -> Cart:
        logger.log("user %s called view_cart", username)
        return self.user_manager.view_cart(username)

    def logout(self, username):
        return self.user_manager.logout(username)

    def view_purchases(self, username):
        logger.log("user %s called view_purchases", username)
        return self.user_manager.view_purchases(username)

    def add_product(self, username, store_id, product_name, quantity):
        logger.log("user %s called add product with store_id:%d, product_name:%s, quantity:%d", username, store_id,
                   product_name, quantity)
        product = self.get_product_from_store(store_id, product_name)
        return self.user_manager.add_product(username, store_id, product, quantity)

    def remove_product(self, username, store_id, product_name, quantity):
        logger.log("user %s called remove product with store_id:%d, product_name:%s, quantity:%d", username, store_id,
                   product_name, quantity)
        product = self.get_product_from_store(store_id, product_name)
        return self.user_manager.remove_product(username, store_id, product, quantity)

    def get_product_from_store(self, store_id, product_name):
        return self.stores_manager.get_product_from_store(store_id, product_name)

    def get_cart(self, username):
        return self.user_manager.get_cart(username)

    def view_purchases_admin(self, username, admin):
        logger.log("admin %s called view_purchases_admin for user %s", admin, username)
        return self.user_manager.view_purchases_admin(username, admin)

    def is_admin(self, username):
        return self.user_manager.is_admin(username)

    def add_managed_store(self, username, store_id):
        return self.user_manager.add_managed_store(username, store_id)

    def remove_managed_store(self, username, store_id):
        return self.user_manager.remove_managed_store(username, store_id)

    def get_managed_stores(self, username):
        return self.user_manager.get_managed_stores(username)

    def check_if_registered(self, username):
        return self.user_manager.check_if_registered(username)

    def check_if_loggedin(self, username):
        return self.user_manager.check_if_loggedin(username)

    def add_purchase(self, username, purchase):
        return self.user_manager.add_purchase(username, purchase)

    def remove_cart(self, username):
        return self.user_manager.remove_cart(username)

    def is_store_manager(self, username):
        return self.user_manager.is_store_manager(username)
