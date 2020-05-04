from project.domain_layer.external_managment.Purchase import Purchase
from project.domain_layer.stores_managment.StoresManager import StoresManager
from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.Store import Store
from spellchecker import SpellChecker

from project import logger


class StoresManagerInterface:
    def __init__(self, users_manager):
        self.stores_manager = StoresManager()
        self.spell_checker = SpellChecker()
        self.users_manager = users_manager

    def search_product(self, search_term: str = "", categories: [str] = [], key_words: [str] = []) \
            -> {int: [Product]}:
        """

        Args:
            search_term:
            categories:
            key_words:

        Returns:

        """
        logger.log("called search with search term:%s, categories:%s, key words:%s", search_term, categories, key_words)
        return self.stores_manager.search(self.spell_checker.correction(search_term),
                                          [self.spell_checker.correction(word) for word in categories],
                                          [self.spell_checker.correction(word) for word in key_words])

    def add_purchase_to_store(self, store_id: int, purchase: Purchase):

        return self.stores_manager.add_purchase_to_store(store_id, purchase)

    # def search(self, search_term: str = "", categories: [str] = None, key_words: [str] = None) -> {Store: [Product]}:
    #     return self.stores_manager.search(search_term, categories, key_words)

    def add_product_to_store(self, store_id: int, user_name: str, product_name: str, product_price: int,
                             product_categories: [str],
                             key_words: [str], amount) -> bool:
        logger.log(
            "user %s called add product to store no.%d. product name:%s"
            " product price:%d product categories:%s,key words:%s, amount:%d",
            user_name, store_id, product_name, product_price, product_categories, key_words, amount)

        if store_id in self.users_manager.get_managed_stores(user_name):
            return self.stores_manager.add_product_to_store(store_id, user_name, product_name, product_price,
                                                            product_categories, key_words, amount)
        return False

    def appoint_manager_to_store(self, store_id, owner, to_appoint):
        logger.log("user %s call appoint manager %s to store no.%d", owner, to_appoint, store_id)
        if store_id in self.users_manager.get_managed_stores(owner) and self.users_manager.check_if_registered(
                to_appoint):
            if self.stores_manager.appoint_manager_to_store(store_id, owner, to_appoint):
                self.users_manager.add_managed_store(to_appoint, store_id)
                return True

        return False

    def appoint_owner_to_store(self, store_id, owner, to_appoint):
        logger.log("user %s call appoint owner %s to store no.%d", owner, to_appoint, store_id)
        if store_id in self.users_manager.get_managed_stores(owner) and self.users_manager.check_if_registered(
                to_appoint):
            if self.stores_manager.appoint_owner_to_store(store_id, owner, to_appoint):
                self.users_manager.add_managed_store(to_appoint, store_id)
                return True

        return False

    def add_permission_to_manager_in_store(self, store_id, owner, manager, permission: str):
        logger.log("user %s add %s permission to %s in store no.%d", owner, permission, manager, store_id)
        if store_id in self.users_manager.get_managed_stores(
                owner) and store_id in self.users_manager.get_managed_stores(manager):
            return self.stores_manager.add_permission_to_manager_in_store(store_id, owner, manager, permission)
        return False

    def remove_permission_from_manager_in_store(self, store_id, owner, manager, permission: str):
        logger.log("user %s remove %s permission to %s in store no.%d", owner, permission, manager, store_id)
        if store_id in self.users_manager.get_managed_stores(
                owner) and store_id in self.users_manager.get_managed_stores(manager):
            self.stores_manager.remove_permission_from_manager_in_store(store_id, owner, manager, permission)

    def open_store(self, owner: str, store_name):
        logger.log("user %s open %s store", owner, store_name)
        if self.users_manager.check_if_registered(owner):
            store_id = self.stores_manager.open_store(owner, store_name)
            self.users_manager.add_managed_store(owner, store_id)
            return store_id
        return -1

    def buy(self, cart):
        self.stores_manager.buy(cart)

    def get_sales_history(self, store_id, user) -> [Purchase]:
        logger.log("user %s get sales history of store no.%d", user, store_id)
        if self.users_manager.check_if_registered(user) and (
                store_id in self.users_manager.get_managed_stores(user) or self.users_manager.is_admin(user)):
            return self.stores_manager.get_sales_history(store_id, user, self.users_manager.is_admin(user))

    def remove_product(self, store_id, product_name, username):
        return self.stores_manager.remove_produce_from_store(store_id, product_name, username)

    def add_visible_discount_to_product(self, store_id, product_name, username, start_date, end_date, percent):
        return self.stores_manager.add_visible_discount_to_product(store_id, product_name, username, start_date, end_date, percent)

    def add_conditional_discount_to_product(self, store_id, product_name, username, start_date, end_date, percent, amount_to_apply):
        return self.stores_manager.add_conditional_discount_to_product(store_id, product_name, username, start_date, end_date, percent, amount_to_apply)

    def edit_visible_discount(self, store_id, product_name, username, discount_id, start_date=None, end_date=None, percent=None):
        self.stores_manager.edit_visible_discount_to_product(store_id, product_name, username, discount_id, start_date, end_date,
                                                            percent)

    def edit_conditional_discount(self, store_id, product_name, username, discount_id, start_date=None, end_date=None, percent=None, conditions=None):
        self.stores_manager.edit_conditional_discount_to_product(store_id, product_name, username, discount_id, start_date, end_date,
                                                            percent, conditions)

    def update_product(self, store_id, username, product_name, attribute, updated):
        return self.stores_manager.update_product(store_id, username, product_name, attribute, updated)

    def remove_manager(self, store_id, owner, to_remove):
        if self.stores_manager.remove_manager(store_id, owner, to_remove):
            self.users_manager.remove_managed_store(to_remove,store_id)
            return True
        return False

    def remove_owner(self, store_id, owner, to_remove):
        return self.stores_manager.remove_owner(store_id, owner, to_remove)