from project.domain_layer.users_managment.NullUser import NullUser
from project.domain_layer.users_managment.RegisteredUser import RegisteredUser
from project.domain_layer.users_managment.User import User
from project import logger
import jsonpickle


class UsersManager:

    incremental_id = 0

    def __init__(self):
        self.publisher = None
        self.reg_user_list = {}
        self.guest_user_list = {}
        # maybe dictionary {id, username}
        self.admins = []

    def find_reg_user(self, username) -> RegisteredUser:
        if username in self.reg_user_list.keys():
            user = self.reg_user_list[username]
            return user
        logger.error("registered user with username %s does not exist", username)
        return NullUser()

    def find_user(self, username) -> User:
        if username in self.reg_user_list.keys():
            user = self.reg_user_list[username]
        else:
            if username in self.guest_user_list.keys():
                user = self.guest_user_list[username]
            else:
                logger.error("user with username %s does not exist", username)
                user = NullUser()
        return user

    def register(self, username, new_username):
        check = self.find_reg_user(new_username)
        if isinstance(check, NullUser):
            registered = RegisteredUser(new_username)
            user = self.find_user(username)
            registered.cart = user.cart
            self.reg_user_list[new_username] = registered
            return True
        else:
            return False

# TODO: if login succeeded, return the following json object:
    #  TODO: user = {username: username, managed_stores: [int], purchase_history: [purchase should be json-style too],
    #   notifications: [strings], cart: [basket should be json-style too] }

    def login(self, username: str, login_username: str):
        check = self.find_reg_user(login_username)
        if not (isinstance(check, NullUser)):
            if check.loggedin is True:
                return False
            check.loggedin = True
            self.guest_user_list.pop(username)
            return login_username
        else:
            return False

    # make sure when  user exits system to remove the user from guest user list
    def add_guest_user(self):
        user = User("guestUser" + str(self.incremental_id))
        self.incremental_id += 1
        self.guest_user_list[user.username] = user
        logger.log("guest user with username %s was added to system", user.username)
        return user.username

    # look up via usr id change user list to map of ids and user
    def view_cart(self, username):
        user = self.find_user(username)
        return jsonpickle.encode(user.cart)

    def logout(self, username):
        user = self.find_reg_user(username)
        if user.loggedin:
            user.logout()
            return self.add_guest_user()
        return username

    def view_purchases(self, username):
        return jsonpickle.encode(self.find_user(username).view_purchase_history())
        # if view purchases of username

    def add_product(self, username, store_id, product, quantity):
        user = self.find_user(username)
        return user.add_product(store_id, jsonpickle.decode(product), quantity)

    # TODO: remove product receive actual product. change to product_name
    def remove_product(self, username, store_id, product, quantity) -> bool:
        user = self.find_user(username)
        return user.remove_product(store_id, jsonpickle.decode(product), quantity)

    def get_cart(self, username):
        user = self.find_user(username)
        return jsonpickle.encode(user.get_cart())

    def view_purchases_admin(self, username, admin):
        if admin in self.admins:
            return jsonpickle.encode(self.find_reg_user(username).view_purchase_history())
        return False

    def is_admin(self, username):
        return username in self.admins

    def add_managed_store(self, username, store_id) -> bool:
        user = self.find_reg_user(username)
        return user.add_managed_store(store_id)

    def get_managed_stores(self, username):
        user = self.find_reg_user(username)
        return jsonpickle.encode(user.get_managed_store())

    def check_if_registered(self, username):
        return username in self.reg_user_list.keys()

    def check_if_loggedin(self, username):
        user = self.find_reg_user(username)
        return user.loggedin

    def add_purchase(self, username, purchase):
        user = self.find_user(username)
        user.add_purchase(jsonpickle.decode(purchase))

    def remove_cart(self, username):
        user = self.find_user(username)
        user.remove_cart()

    def remove_managed_store(self, username, store_id) -> bool:
        user = self.find_reg_user(username)
        return user.remove_managed_store(store_id)

    def add_notification(self, loggedout_username, message):
        self.find_reg_user(loggedout_username).add_notification(message)

    def have_notifications(self, username):
        return self.find_reg_user(username).have_notifications()

    def get_user_notifications(self, username):
        return self.find_reg_user(username).get_notifications()

    def is_store_manager(self, username) -> bool:
        reg_user = self.find_reg_user(username)
        return reg_user.is_store_manager()
