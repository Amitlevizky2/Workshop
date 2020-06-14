import jsonpickle
import jsons

from project.domain_layer.users_managment.Cart import Cart
from project.domain_layer.users_managment.UsersManager import UsersManager
from project import logger
from project.service_layer import StoresManagerInterface
from project.service_layer.Security import Security


class UsersManagerInterface:
    security = Security()

    def __init__(self):
        self.user_manager = UsersManager()
        self.stores_manager = None
        username = self.user_manager.add_guest_user()
        print(username)
        self.user_manager.register(username, "admin")
        self.user_manager.admins.append("admin")

    def set_stores_manager(self, stores_manager: StoresManagerInterface):
        self.stores_manager = stores_manager

    def register(self, username, new_username, password):
        logger.log("user %s called register with new_username:%s", username, new_username)
        ans, data = self.user_manager.register(username, new_username)
        if ans is True:
            self.security.add_user(new_username, password)
        print(data)
        return ans, data

# TODO: remove the return type hint. does not necessarily returns bool
    # EVERYTIME SOMEONE OPENS THE SYSTEM A NEW USER IS CREATEDDDDDDDD
    def login(self, username: str, login_username: str, password):
        print("here!")
        logger.log("user %s called login with login_username:%s", username, login_username)
        if self.security.verify_password(login_username, password):
            logged_in, data = self.user_manager.login(username, login_username)
            print(data)
            if logged_in is True:
                user = jsons.loads(data['data'])
                managed_stores = []
                print(user)
                for store in user['managed_stores']:
                    store_description = self.stores_manager.get_store_description(store['store_id'])
                    managed_stores.append(store_description)
                user['managed_stores'] = managed_stores
                print("******************")
                print(user)
                return logged_in, {'data': user}
        else:
            print("!!!!!!!!!!!")
            return False, {'error_msg': 'incorrect password. Try again.'}

    def add_guest_user(self):
        return self.user_manager.add_guest_user()

# TODO: view_cart returns json object, not Cart.
    # look up via usr id change user list to map of ids and user
    def view_cart(self, username):
        logger.log("user %s called view_cart", username)
        res, cart = self.user_manager.get_cart(username)
        if res is True:
            user_cart = jsonpickle.decode(cart)
            cart_view = jsons.loads(self.stores_manager.get_cart_description(user_cart))
            return ({
                'error': False,
                'data': cart_view
            })
        return ({
            'error': True,
            'error_msg': cart
        })

    def logout(self, username):
        return self.user_manager.logout(username)

    def view_purchases(self, username):
        logger.log("user %s called view_purchases", username)
        return self.user_manager.view_purchases(username)

# TODO: change product to product_name and get the actual product from the method i added in StoresManagerInterface
    def add_product(self, username, store_id, product_name, quantity) -> bool:
        logger.log("user %s called add product with store_id:%d, product_name:%s, quantity:%d", username, store_id, product_name, quantity)
        return self.user_manager.add_product(username, store_id, product_name, quantity)

    # TODO: remove_product receive actual product. change to product_name
    def remove_product(self, username, store_id, product, quantity):
        """
        :param username:
        :param store_id:
        :param product:
        :param quantity:
        :return: True if product was removed. False otherwise.
        """
        logger.log("user %s called remove product with store_id:%d, product_name:%s, quantity:%d", username, store_id,
                   product.name, quantity)
        return self.user_manager.remove_product(username, store_id, product, quantity)

    def get_product_from_store(self, store_id, product_name):
        return self.stores_manager.get_product_from_store(store_id, product_name)

    def get_cart(self, username):
        answer, data = self.user_manager.get_cart(username)
        if answer is False:
            return answer, data
        return answer, jsonpickle.decode(data)

    def view_purchases_admin(self, username, admin):
        logger.log("admin %s called view_purchases_admin for user %s", admin, username)
        return self.user_manager.view_purchases_admin(username, admin)

    def is_admin(self, username):
        answer = self.user_manager.is_admin(username)
        return {
            'error': False,
            'data': answer
        }

    def add_managed_store(self, username, store_id):
        """
        :param username:
        :param store_id:
        :return:
        """
        return self.user_manager.add_managed_store(username, store_id)

    def remove_managed_store(self, username, store_id):
        return self.user_manager.remove_managed_store(username, store_id)

    def get_managed_stores_description(self, username):
        ans = jsons.loads(self.user_manager.get_managed_stores(username))
        if ans.error is False:
            stores_des = []
            for store in ans.data:
                res_store = self.stores_manager.get_store_description(store)
                print(res_store)
                stores_des.append(res_store)
            return ({
                'error': False,
                'data': stores_des
            })
        else:
            return({
                'error': True,
                'error_msg': ans.error_msg
            })

    def get_managed_stores(self, username):
        ans = jsons.loads(self.user_manager.get_managed_stores(username))
        if ans.error is True:
            return []
        return ans.data

    def get_stores_managed_by_user(self, username):
        return self.user_manager.get_managed_stores(username)

    def check_if_registered(self, username):
        return self.user_manager.check_if_registered(username)

    def check_if_loggedin(self, username):
        return self.user_manager.check_if_loggedin(username)

    def add_purchase(self, username, purchases):
        return self.user_manager.add_purchase(username, jsonpickle.encode(purchases))

    def remove_cart(self, username):
        return self.user_manager.remove_cart(username)

    def is_store_manager(self, username):
        return self.user_manager.is_store_manager(username)

    def get_users_manager(self) -> UsersManager:
        return self.user_manager


