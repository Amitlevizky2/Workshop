from project.domain_layer.users_managment.Cart import Cart
from project.domain_layer.users_managment.UsersManager import UsersManager


class UsersManagerInterface:

    def __init__(self):
        self.user_manager = UsersManager()

    def register(self, username, new_username, password):
        return self.user_manager.register(username, new_username,password)

    ##EVERYTIME SOMEONE OPENS THE SYSTEM A NEW USER IS CREATEDDDDDDDD
    def login(self, username: str, login_username: str, password) -> bool:
        return self.user_manager.login(username, login_username, password)

    def add_guest_user(self):
        return self.user_manager.add_guest_user()

    # look up via usr id change user list to map of ids and user
    def view_cart(self, username) -> Cart:
        return self.user_manager.view_cart(username)

    def logout(self, username):
        return self.user_manager.logout(username)

    def view_purchases(self, username):
        return self.user_manager.view_purchases(username)

    def add_product(self, username, store_id, product, quantity):
        return self.user_manager.add_product(username,store_id, product, quantity)

    def remove_product(self, username, store_id, product, quantity):
        return self.user_manager.remove_product(username,store_id, product, quantity)

    def get_cart(self, username):
        return self.user_manager.get_cart(username)

    def view_purchases_admin(self, username, admin):
        return self.user_manager.view_purchases_admin(username, admin)

    def is_admin(self,username):
        return self.user_manager.is_admin(username)

    def add_managed_store(self, username, store_id):
        return self.user_manager.add_managed_store(username, store_id)

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