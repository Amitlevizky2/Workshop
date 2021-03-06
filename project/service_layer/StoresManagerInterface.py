from datetime import datetime

import jsons
# from spellchecker import SpellChecker

from project import logger
from project.domain_layer.communication_managment import Publisher
from project.domain_layer.external_managment.Purchase import Purchase
from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.StoresGetters import StoresGetters
from project.domain_layer.stores_managment.StoresManager import StoresManager


class StoresManagerInterface:
    def __init__(self, users_manager, data_handler):
        self.stores_manager = StoresManager(data_handler)
        self.stores_getters = StoresGetters(self.stores_manager)
        # self.spell_checker = SpellChecker()
        self.users_manager = users_manager
        self.publisher = None

    def search_product(self, search_term: str = "", categories: [str] = [], key_words: [str] = []):
        """

        Args:
            search_term:
            categories:
            key_words:

        Returns:

        """
        logger.log("called search with search term:%s, categories:%s, key words:%s", search_term, categories, key_words)
        return self.stores_manager.search(search_term,
                                          [word for word in categories],
                                          [word for word in key_words])

        # return self.stores_manager.search(self.spell_checker.correction(search_term),
        #                                   [self.spell_checker.correction(word) for word in categories],
        #                                   [self.spell_checker.correction(word) for word in key_words])

    def add_purchase_to_store(self, store_id: int, purchase: Purchase):
        store_id = int(store_id)
        return self.stores_manager.add_purchase_to_store(store_id, purchase)

    def search(self, search_term: str = "", categories: [str] = [], key_words: [str] = []):
        return self.stores_manager.search(search_term, categories, key_words)

    def add_product_to_store(self, store_id: int, user_name: str, product_name: str, product_price: int,
                             product_categories: [str],
                             key_words: [str], amount):
        store_id = int(store_id)
        logger.log(
            "user %s called add product to store no.%s. product name:%s"
            " product price:%s product categories:%s,key words:%s, amount:%s",
            user_name, store_id, product_name, product_price, product_categories, key_words, amount)
        if store_id in self.users_manager.get_managed_stores(user_name):
            return jsons.loads(
                self.stores_manager.add_product_to_store(store_id, user_name, product_name, product_price,
                                                         product_categories, key_words, amount))
        return {
            'error': True,
            'error_msg': 'User ' + user_name + ' is not associated with the store.'
        }

    def appoint_manager_to_store(self, store_id, owner, to_appoint):
        store_id = int(store_id)
        logger.log("user %s call appoint manager %s to store no.%d", owner, to_appoint, store_id)
        if store_id in self.users_manager.get_managed_stores(owner) and self.users_manager.check_if_registered(
                to_appoint):
            appointment = jsons.loads(self.stores_manager.appoint_manager_to_store(store_id, owner, to_appoint))
            if appointment['error'] is False:
                self.users_manager.add_managed_store(to_appoint, store_id)
            return appointment
        return {
            'error': True,
            'error_msg': 'error'
        }

    def appoint_owner_to_store(self, store_id, owner, to_appoint):
        store_id = int(store_id)
        logger.log("user %s call appoint owner %s to store no.%d", owner, to_appoint, store_id)
        stores = self.users_manager.get_managed_stores(owner)
        if store_id in stores and self.users_manager.check_if_registered(to_appoint):
            appointment = jsons.loads(self.stores_manager.appoint_owner_to_store(store_id, owner, to_appoint))
            if appointment['error'] is False:
                self.users_manager.add_managed_store(to_appoint, store_id)
            return appointment
        return {
            'error': True,
            'error_msg': 'error'
        }

    def add_permission_to_manager_in_store(self, store_id, owner, manager, permission: str):
        store_id = int(store_id)
        logger.log("user %s add %s permission to %s in store no.%d", owner, permission, manager, store_id)
        if store_id in self.users_manager.get_managed_stores(
                owner) and store_id in self.users_manager.get_managed_stores(manager):
            return self.stores_manager.add_permission_to_manager_in_store(store_id, owner, manager, permission)
        return {
            'error': True,
            'error_msg': 'error'
        }

    def edit_store_manager_permissions(self, store_id, owner, manager, permissions):
        store_id = int(store_id)
        logger.log("user %s remove %s permission to %s in store no.%d", owner, permissions, manager, store_id)
        if store_id in self.users_manager.get_managed_stores(
                owner) and store_id in self.users_manager.get_managed_stores(manager):
            return self.stores_manager.edit_store_manager_permissions(store_id, owner, manager, permissions)
        return jsons.dumps({
            'error': True,
            'error_msg': 'error'
        })

    # TODO: DOSE NOT RETURN A VALUE.
    def remove_permission_from_manager_in_store(self, store_id, owner, manager, permission: str):
        store_id = int(store_id)
        logger.log("user %s remove %s permission to %s in store no.%d", owner, permission, manager, store_id)
        if store_id in self.users_manager.get_managed_stores(
                owner) and store_id in self.users_manager.get_managed_stores(manager):
            return self.stores_manager.remove_permission_from_manager_in_store(store_id, owner, manager, permission)
        return jsons.dumps({
            'error': True,
            'error_msg': 'error'
        })

    def open_store(self, owner: str, store_name):
        logger.log("user %s open %s store", owner, store_name)
        if self.users_manager.check_if_registered(owner):
            store_id = self.stores_manager.open_store(owner, store_name)
            self.users_manager.add_managed_store(owner, store_id)
            return store_id
        return -1

    def buy(self, cart):
        return self.stores_manager.buy(cart)

    def get_sales_history(self, store_id, user) -> [Purchase]:
        store_id = int(store_id)
        logger.log("user %s get sales history of store no.%d", user, store_id)
        managed_stores = self.users_manager.get_managed_stores(user)
        print(managed_stores)
        print(store_id)
        if self.users_manager.check_if_registered(user) and (
                store_id in managed_stores or self.users_manager.is_admin(user)['data']):
            return self.stores_manager.get_sales_history(store_id, user, self.users_manager.is_admin(user)['data'])
        return jsons.dumps({'error': True, 'error_msg': 'error'})

    def remove_product(self, store_id, product_name, username):
        store_id = int(store_id)
        return self.stores_manager.remove_product_from_store(store_id, product_name, username)

    # def add_discount_to_product(self, store_id, product_name, username, start_date, end_date, percent):
    #     return self.stores_manager.add_discount_to_product(store_id, product_name, username, start_date, end_date, percent)

    def update_product(self, store_id, username, product_name, new_price, new_amount):
        """
        :param store_id: the store we want to update
        :param username: the user who wants to update
        :param product_name: product to update
        :param new_price: the parameter we wants to update
        :param new_amount: new value
        :return: True if succeed
        """
        store_id = int(store_id)
        new_price = int(new_price)
        new_amount = int(new_amount)
        return self.stores_manager.update_product(store_id, username, product_name, new_price, new_amount)

    # TODO: CHANGE RETURN VALS.
    def remove_manager(self, store_id, owner, to_remove):
        store_id = int(store_id)
        if self.stores_manager.remove_manager(store_id, owner, to_remove):
            self.users_manager.remove_managed_store(to_remove, store_id)
            return True
        return False

    def remove_owner(self, store_id, owner, to_remove):
        store_id = int(store_id)
        return self.stores_manager.remove_owner(store_id, owner, to_remove)

    def add_purchase_store_policy(self, store_id: int = None, permitted_user: str = None,
                                  min_amount_products: int = None, max_amount_products: int = None):
        _min_amount_products = int(min_amount_products)
        _max_amount_products = int(max_amount_products)
        store_id = int(store_id)
        return self.stores_manager.add_purchase_store_policy(store_id, permitted_user, _min_amount_products,
                                                             _max_amount_products)

    def add_purchase_product_policy(self, store_id: int = None, permitted_user: str = None,
                                    min_amount_products: int = None,
                                    max_amount_products: int = None, products: list = []):
        store_id = int(store_id)

        return self.stores_manager.add_purchase_product_policy(store_id, permitted_user, min_amount_products,
                                                               max_amount_products, products)

    def add_purchase_composite_policy(self, store_id: int = None, permitted_user: str = None,
                                      purchase_policies_id=None,
                                      logic_operator: str = None):
        store_id = int(store_id)
        return self.stores_manager.add_purchase_composite_policy(store_id, permitted_user, purchase_policies_id, logic_operator)

    def add_policy_to_purchase_composite_policy(self, store_id: int = None, permitted_user: str = None,
                                                composite_id: int = None,
                                                policy_id: int = None):
        store_id = int(store_id)
        policy_id = int(policy_id)
        return self.stores_manager.add_policy_to_purchase_composite_policy(store_id, permitted_user, composite_id,
                                                                           policy_id)

    def add_product_to_purchase_product_policy(self, store_id: int = None, policy_id: int = None,
                                               permitted_user: str = None,
                                               product_name: str = None):
        store_id = int(store_id)
        policy_id = int(policy_id)
        return self.stores_manager.add_product_to_purchase_product_policy(store_id, policy_id, permitted_user,
                                                                          product_name)

    def remove_purchase_policy(self, store_id: int = None, permitted_user: str = None, policy_id: int = None):
        store_id = int(store_id)
        policy_id = int(policy_id)
        return self.stores_manager.remove_purchase_policy(store_id, permitted_user, policy_id)

    def remove_product_from_purchase_product_policy(self, store_id: int = None, policy_id: int = None,
                                                    permitted_user: str = None,
                                                    product_name: str = None):
        store_id = int(store_id)
        policy_id = int(policy_id)
        return self.stores_manager.remove_product_from_purchase_product_policy(store_id, policy_id, permitted_user,
                                                                               product_name)

    def get_discounts(self, store_id: int = None):
        answer = jsons.loads(self.stores_getters.get_store_discounts("", store_id))
        discounts = answer['desc']
        print(discounts)

        for discount in discounts.keys():
            print(discounts[discount].keys())
            discounts[discount]['products_in_discount'] = [*discounts[discount]['products_in_discount'].keys()]
        answer['desc'] = discounts
        return jsons.dumps(answer)

    def get_discount_details(self, store_id: int = None, discount_id: int = None):
        return self.stores_getters.get_store_discount('', store_id, discount_id)

    def get_purchases_policies(self, store_id: int = None):
        return self.stores_getters.get_purchases_policies('', store_id)

    def get_purchase_policy_details(self, store_id: int = None, purchase_policy_id: int = None):
        return self.stores_getters.get_purchase_policy('', store_id, purchase_policy_id)

    def get_cart_description(self, cart=None):  # NEED_TO_CHECK
        return self.stores_manager.get_cart_description(cart)

    def get_updated_basket(self, basket=None):
        return self.stores_manager.get_updated_basket(basket)

    def add_visible_discount_to_product(self, store_id: int = None, username: str = None, start_date=None,
                                        end_date=None, percent: int = None, products: [str] = None):
        print(start_date[0:10])
        _start_date = datetime.strptime(start_date[0:10], '%Y-%m-%d')
        _end_date = datetime.strptime(end_date[0:10], '%Y-%m-%d')
        _percent = int(percent)
        store_id = int(store_id)
        return self.stores_manager.add_visible_product_discount(store_id, username, _start_date, _end_date, _percent,
                                                                products)

    def add_conditional_discount_to_product(self, store_id: int = None, username: str = None, start_date=None,
                                            end_date=None, percent: int = None,
                                            min_amount: int = None, num_prods_to_apply: int = None,
                                            products: list = []):
        _start_date = datetime.strptime(start_date[0:10], '%Y-%m-%d')
        _end_date = datetime.strptime(end_date[0:10], '%Y-%m-%d')
        _percent = int(percent)
        if min_amount:
            min_amount = int(min_amount)
        if num_prods_to_apply:
            num_prods_to_apply = int(num_prods_to_apply)
        store_id = int(store_id)

        return self.stores_manager.add_conditional_discount_to_product(store_id, username, _start_date, _end_date,
                                                                       _percent, min_amount, num_prods_to_apply,
                                                                       products)

    def add_conditional_discount_to_store(self, store_id: int = None, username: str = None, start_date=None,
                                          end_date=None, percent: int = None,
                                          min_price: int = None):
        _start_date = datetime.strptime(start_date[0:10], '%Y-%m-%d')
        _end_date = datetime.strptime(end_date[0:10], '%Y-%m-%d')
        _percent = int(percent)
        _min_price = int(min_price)
        store_id = int(store_id)

        return self.stores_manager.add_conditional_discount_to_store(store_id, username, _start_date, _end_date,
                                                                     _percent, _min_price)

    def add_product_to_discount(self, store_id: int = None, permitted_user: str = None, discount_id: int = None,
                                product_name: str = None):
        store_id = int(store_id)
        discount_id = int(discount_id)
        return self.stores_manager.add_product_to_discount(store_id, permitted_user, discount_id, product_name)

    def remove_product_from_discount(self, store_id: int = None, permitted_user: str = None,
                                     discount_id: int = None, product_name: str = None):
        store_id = int(store_id)
        discount_id = int(discount_id)
        return self.stores_manager.remove_product_from_discount(store_id, permitted_user, discount_id, product_name)

    def add_composite_discount(self, store_id: int = None, username: str = None, start_date=None,
                               end_date=None, logic_operator: str = None,
                               discounts_products_dict: dict = None,
                               discounts_to_apply_id: list = None):  # discounts_products_dict = {discount_id, [products_names]}
        _start_date = datetime.strptime(start_date[0:10], '%Y-%m-%d')
        _end_date = datetime.strptime(end_date[0:10], '%Y-%m-%d')
        store_id = int(store_id)
        return self.stores_manager.add_composite_discount(store_id, username, _start_date, _end_date, logic_operator,
                                                          discounts_products_dict, discounts_to_apply_id)

    def edit_visible_discount_to_products(self, store_id: int = None, username: str = None,
                                          discount_id: int = None, start_date=None, end_date=None,
                                          percent: int = None, products=[]):
        _start_date = datetime.strptime(start_date[0:10], '%Y-%m-%d')
        _end_date = datetime.strptime(end_date[0:10], '%Y-%m-%d')
        _percent = int(percent)
        store_id = int(store_id)
        return self.stores_manager.edit_visible_discount_to_products(store_id, username, discount_id, _start_date,
                                                                     _end_date, percent, products)

    def edit_conditional_discount_to_product(self, store_id: int = None, discount_id: int = None, username: str = None,
                                             start_date=None, end_date=None,
                                             percent: int = None, min_amount: int = None, nums_to_apply: int = None,
                                             products=[]):
        _start_date = datetime.strptime(start_date[0:10], '%Y-%m-%d')
        _end_date = datetime.strptime(end_date[0:10], '%Y-%m-%d')
        percent = int(percent)
        nums_to_apply = int(nums_to_apply)
        min_amount = int(min_amount)
        store_id = int(store_id)
        return self.stores_manager.edit_conditional_discount_to_product(store_id, discount_id, username, _start_date,
                                                                        _end_date, percent, min_amount, nums_to_apply,
                                                                        products)

    # endless recursive function
    def edit_conditional_discount_to_store(self, store_id: int = None, discount_id: int = None, username: str = None,
                                           start_date=None, end_date=None,
                                           percent: int = None,
                                           min_price: int = None):
        _start_date = datetime.strptime(start_date[0:10], '%Y-%m-%d')
        _end_date = datetime.strptime(end_date[0:10], '%Y-%m-%d')
        _percent = int(percent)
        _min_price = int(min_price)
        store_id = int(store_id)
        return self.stores_manager.edit_conditional_discount_to_store(store_id, discount_id, username, _start_date,
                                                                      _end_date, _percent,
                                                                      _min_price)

    def get_store_description(self, store_id):
        return self.stores_getters.get_store_description(store_id)

    def get_stores(self):
        return self.stores_getters.get_stores_description()

    def get_inventory_description(self, store_id):
        return self.stores_getters.get_inventory_description('', store_id)

    def get_store_owners(self, store_id):
        """
        :param store_id:
        :return: array of store owners user names
        """
        return self.stores_getters.get_store_owners('', store_id)

    def get_store_managers(self, store_id):
        """
        :param store_id:
        :return: array of store managers user names
        """
        return self.stores_getters.get_store_managers('', store_id)

    def get_product_from_store(self, store_id, product_name) -> Product:
        return self.stores_getters.get_product_from_store('', store_id, product_name)

    def bound_publisher(self, publisher: Publisher):
        self.stores_manager.bound_publisher(publisher)

    def get_stores_manager(self) -> StoresManager:
        return self.stores_manager

    def check_cart_validity(self, cart):
        return self.stores_manager.check_cart_validity(cart)

    def get_user_permissions(self, store_id, username):
        return self.stores_manager.get_user_permissions(store_id, username)

    def is_valid_amount(self, store_id, product_name, quantity):
        return self.stores_manager.is_valid_amount(store_id, product_name, quantity)

    def init_data(self):
        self.stores_manager.init_data()