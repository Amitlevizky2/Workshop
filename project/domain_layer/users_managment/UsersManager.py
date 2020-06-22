import jsons

from project.domain_layer.users_managment.Cart import Cart
# from project.domain_layer.stores_managment.StoresManager import StoresManager
from project.domain_layer.users_managment.NullUser import NullUser
from project.domain_layer.users_managment.RegisteredUser import RegisteredUser
from project.domain_layer.users_managment.Statistics import Statistics
from project.domain_layer.users_managment.User import User
from project import logger
import jsonpickle


class UsersManager:
    # store_manager = StoresManager()
    incremental_id = 0

    def __init__(self):
        # self.publisher = None
        #  self.stores_manager = None
        self.reg_user_list = {}

        self.guest_user_list = {}
        # maybe dictionary {id, username}
        self.admins = []
        self.stats = Statistics()

    def find_reg_user(self, username):
        if username in self.reg_user_list.keys():
            user = self.reg_user_list[username]
            return True, user
        logger.error("registered user with username %s does not exist", username)
        return False, {'error_msg': 'User ' + username + ' does not exist.'}

    def find_user(self, username):
        print(type(username))

        if username in self.reg_user_list.keys():
            user = self.reg_user_list[username]
            return True, user
        else:
            if username in self.guest_user_list.keys():
                user = self.guest_user_list[username]
                return True, user
            else:
                logger.error("user with username %s does not exist", username)
                return False, {'error_msg ': 'user not found'}

    def register(self, username, new_username):
        ans, data = self.find_reg_user(new_username)
        if ans is False:
            # isinstance(check, NullUser):
            registered = RegisteredUser(new_username)
            # change fined_user() return vals
            res, user = self.find_user(username)
            if res is True:
                registered.cart = user.cart
                self.reg_user_list[new_username] = registered
                return True, {
                    'data': 'Thank you for joining us ' + new_username +
                            '! To continue as ' + new_username + ' please login.'}
            return res, user
        else:
            return False, {
                'error_msg': 'User name: ' + new_username + ' is already in use. Please choose another user name.'}

    def login(self, username: str, login_username: str):
        ans, data = self.find_reg_user(login_username)
        if ans is True:
            if data.loggedin is True:
                return False, {'error_msg': 'user ' + data.username + ' is already logged in.'}
            data.loggedin = True
            res, guest_user = self.find_user(username)
            if res is True:
                self.merge_carts(data, guest_user.cart)
                self.guest_user_list.pop(username)
                self.update_stats(username)
                return True, {'data': data.get_jsn_description()}
            return res, guest_user
        else:
            return False, {'error_msg': 'incorrect user name. Please try again.'}

    def update_stats(self, username: str):
        self.stats.add_reg_users()
        self.stats.remove_guests_stats()

        if self.is_manager(username):
            self.stats.add_managers()

    def is_manager(self, username: str):
        ans: RegisteredUser = self.find_reg_user(username)
        if ans.is_store_manager():
            return True
        return False

    # make sure when  user exits system to remove the user from guest user list
    def add_guest_user(self):
        user = User("guestUser" + str(self.incremental_id))
        self.incremental_id += 1
        self.guest_user_list[user.username] = user
        logger.log("guest user with username %s was added to system", user.username)
        self.stats
        return user.username

    # look up via usr id change user list to map of ids and user
    def view_cart(self, username):
        ans, user = self.find_user(username)
        if ans is True:
            return jsonpickle.encode(user.view_cart())
        else:
            return None

    def logout(self, username):
        ans, user = self.find_reg_user(username)
        if ans is True:
            if user.loggedin is True:
                user.logout()
                return {'error': False, 'data': self.add_guest_user()}
            return {'error': True, 'error_msg': 'User ' + username + ' is not logged in.'}
        return {'error': True, 'error_msg': ans['error_msg']}

    def view_purchases(self, username):
        ans, user = self.find_user(username)
        if ans is True:
            return True, user.view_purchase_history(view_format='json')
        else:
            return False, user
        # if view purchases of username

    def add_product(self, username, store_id, product, quantity):
        ans, user = self.find_user(username)

        if ans is True:
            return user.add_product(store_id, product, quantity)
        else:
            return False

    def remove_product(self, username, store_id, product, quantity):
        answer, user = self.find_user(username)
        if answer is True:
            ans = user.remove_product(store_id, product, quantity)
            if ans is True:
                data = {'data': 'product ' + product + ' quantity was updated'}
                return ans, data
            else:
                data = {'error_msg': 'product ' + product + ' is not in cart'}
                return ans, data

    def get_cart(self, username):
        ans, user = self.find_user(username)
        if ans is True:
            cart = user.get_cart()
            return ans, jsonpickle.encode(cart)
        else:
            return ans, user

    # def view_cart_after_discount(self, username: str):
    #      updated_baskets_list = []
    #      baskets = self.get_cart(username).baskets
    #
    #      for basket in baskets.values():
    #          basket_prices = self.stores_manager.calculate_basket_price(basket)
    #          updated_baskets_list.append(basket_prices)
    #
    #      return updated_baskets_list

    def view_purchases_admin(self, username, admin):
        ans, user = self.find_reg_user(username)
        if admin in self.admins:
            if ans is True:
                return jsonpickle.encode(user.view_purchase_history())
            else:
                return False, user
        return False, {'error_msg': 'user ' + admin + ' is not an admin'}

    def add_admin(self, admin, username_to_be_admin):
        if self.find_reg_user(username_to_be_admin)[0]:
            if self.is_admin(admin):
                if not self.is_admin(username_to_be_admin):
                    self.admins.append(username_to_be_admin)
                else:
                    return False, {'error_msg': 'user' + username_to_be_admin + 'is allready admin'}
            else:
                return False,{'error_msg': 'user ' + admin + ' is not an admin'}
        else:
            return False, {'error_msg': 'user ' + username_to_be_admin + ' is not an registered user'}

    def is_admin(self, username):
        return username in self.admins


    def add_managed_store(self, username, store_id):
        ans, user = self.find_reg_user(username)
        if ans is True:
            added = user.add_managed_store(store_id)
            if added is True:
                return True, {'data': 'appointed successfully'}
            return False, {'error_msg': 'user ' + user + ' is already managing the store: ' + store_id + '.'}
        return ans, user

    def get_managed_stores(self, username, view_format=''):
        ans, user = self.find_reg_user(username)
        if ans is True:
            return jsons.dumps({
                'error': False,
                'data': user.get_managed_store()})
        return jsons.dumps({
            'error': True,
            'error_msg': user
        })

    def check_if_registered(self, username):
        return username in self.reg_user_list.keys()

    def check_if_loggedin(self, username):
        ans, user = self.find_reg_user(username)
        if ans is True:
            return user.loggedin
        return False

    def add_purchase(self, username, purchases):
        ans, user = self.find_user(username)
        if ans is True:
            user.add_purchase(jsonpickle.decode(purchases))
            return True
        else:
            return ans, user

    def remove_cart(self, username):
        ans, user = self.find_user(username)
        if ans is True:
            user.remove_cart()
            return True
        else:
            return False

    def remove_managed_store(self, username, store_id):
        answer, data = self.find_reg_user(username)
        if answer is False:
            return answer, {'error_msg': data}
        return True, {'data': data.remove_managed_store(store_id)}

    def add_notification(self, loggedout_username, message):
        ans, data = self.find_reg_user(loggedout_username)
        if ans is True:
            data.add_notification(message)
            return True
        return False

    def get_user_notifications(self, username):
        ans, data = self.find_reg_user(username)
        if ans is True:
            return data.get_notifications()
        return False

    def merge_carts(self, registered_user: RegisteredUser, cart_to_merge: Cart):
        registered_user.merge_carts(cart_to_merge)
        return True

    # def set_stores_manager(self, stores_manager: StoresManager):
    #     self.stores_manager = stores_manager
    def is_store_manager(self, username):
        pass

    def get_today_stats(self):
        return {
            'error': False,
            'stats': self.stats.get_today_statistics()
        }
