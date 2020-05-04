import logging
from project import logger

from project.domain_layer.external_managment.Purchase import Purchase
from project.domain_layer.stores_managment.Conditions import ProductCondition
from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.Discount import VisibleProductDiscount, ConditionalProductDiscount
from project.domain_layer.stores_managment.Store import Store
from project.domain_layer.users_managment.Cart import Cart
from project.domain_layer.stores_managment.NullStore import NullStore


class StoresManager:
    def __init__(self):
        self.stores = {}
        self.stores_idx = 0

    def update_product(self, store_id, user, product_name, attribute, updated):
        """

        Args:
            store_id: the store we want to update
            user: the user who wants to update
            product_name: product to update
            attribute: the parameter we wants to update
            updated: new value

        Returns:True if succeed

        """
        return self.get_store(store_id).update_product(user, product_name, attribute, updated)

    def search(self, search_term: str = "", categories: [str] = [], key_words: [str] = []) -> {int: [Product]}:
        """

        Args:
            search_term: part of the wanted product name
            categories: categories to search in
            key_words:

        Returns:dist {Store:list of products in store}

        """
        search_result = {}
        for store_id in self.stores.keys():
            search_in_store = self.get_store(store_id).search(search_term, categories, key_words)
            if search_in_store is not None and len(search_in_store) > 0:
                search_result[store_id] = search_in_store
        return search_result

    def get_store(self, store_id: int) -> Store:
        if store_id in self.stores.keys():

            return self.stores.get(store_id)
        else:
            logger.error("%d store id doesn't exist", store_id)
            return NullStore()

    def add_product_to_store(self, store_id: int, user_name: str, product_name: str, product_price: int,
                             product_categories: [str],
                             key_words: [str], amount) -> bool:
        """

        Args:
            amount:
            store_id:
            user_name:
            product_name:
            product_price:
            product_categories:
            key_words:

        Returns:

        """
        return self.get_store(store_id).add_product(user_name, product_name, product_price,
                                                    product_categories, key_words, amount)

    def appoint_manager_to_store(self, store_id, owner, to_appoint):
        """

        Args:
            store_id:
            owner:
            to_appoint:
        """
        return self.get_store(store_id).appoint_manager(owner, to_appoint)

    def appoint_owner_to_store(self, store_id, owner, to_appoint):
        """

        Args:
            store_id:
            owner:
            to_appoint:
        """
        return self.get_store(store_id).appoint_owner(owner, to_appoint)

    def add_permission_to_manager_in_store(self, store_id, owner, manager, permission: str):
        return self.get_store(store_id).add_permission_to_manager(owner, manager, permission)

    def remove_permission_from_manager_in_store(self, store_id, owner, manager, permission: str):
        return self.get_store(store_id).remove_permission_from_manager(owner, manager, permission)

    def add_purchase_to_store(self, store_id: int, purchase: Purchase):
        return self.get_store(store_id).add_new_sale(purchase)

    def open_store(self, owner: str, store_name):
        self.stores[self.stores_idx] = Store(self.stores_idx, store_name, owner)
        self.stores_idx += 1
        return self.stores_idx - 1

    def buy(self, cart: Cart):

        for store in cart.baskets.keys():
            basket = cart.get_basket(store)
            for product in basket.products.keys():
                if not self.get_store(store).buy_product(product, basket.products.get(product)[1]):
                    return False
        return True

    def get_sales_history(self, store_id, user, is_admin) -> [Purchase]:
        return self.get_store(store_id).get_sales_history(user, is_admin)

    def get_store_products(self, store_id):
        return self.get_store(store_id).get_store_products()

    def remove_produce_from_store(self, store_id, product_name, username):
        store = self.get_store(store_id)
        product = store.search(product_name)
        if product:
            return store.remove_product(product_name, username)
        return False

    def add_visible_discount_to_product(self, store_id, product_name, username, start_date, end_date, percent):
        store = self.get_store(store_id)
        return store.add_visible_discount_to_product(product_name, username,
                                                     VisibleProductDiscount(start_date, end_date, percent))

    def add_conditional_discount_to_product(self, store_id, product_name, username, start_date, end_date, percent, amount_to_apply):
        store = self.get_store(store_id)
        condition = ProductCondition(amount_to_apply, percent)
        return store.add_conditional_discount_to_product(product_name, username,
                                                     ConditionalProductDiscount(start_date, end_date, percent, condition))

    def edit_visible_discount_to_product(self, store_id, product_name, username, discount_id, start_date, end_date, percent):
        store = self.get_store(store_id)
        return store.edit_visible_discount(product_name, username, discount_id, start_date, end_date, percent)

    def edit_conditional_discount_to_product(self, store_id, product_name, discount_id, username, start_date, end_date, percent,
                                             conditions):
        store = self.get_store(store_id)
        return store.edit_conditional_discount(product_name, username, discount_id, start_date, end_date, percent, conditions)

    def remove_manager(self, store_id, owner, to_remove):
        store = self.get_store(store_id)
        return store.remove_manager(owner, to_remove)

    def remove_owner(self, store_id, owner, to_remove):
        store = self.get_store(store_id)
        return store.remove_owner(owner, to_remove)



