from project.domain_layer.external_managment.Purchase import Purchase
from project.domain_layer.stores_managment.DiscountsPolicies.LogicOperator import LogicOperator
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

    def update_product(self, store_id, username, product_name, attribute, updated):
        return self.stores_manager.update_product(store_id, username, product_name, attribute, updated)

    def remove_manager(self, store_id, owner, to_remove):
        if self.stores_manager.remove_manager(store_id, owner, to_remove):
            self.users_manager.remove_managed_store(to_remove,store_id)
            return True
        return False

    def remove_owner(self, store_id, owner, to_remove):
        return self.stores_manager.remove_owner(store_id, owner, to_remove)

    def add_purchase_store_policy(self, store_id: int = None, permitted_user: str = None,
                                  min_amount_products: int = None, max_amount_products: int = None):
        return self.stores_manager.add_purchase_store_policy(store_id, permitted_user, min_amount_products, max_amount_products)

    def add_purchase_product_policy(self, store_id: int = None, permitted_user: str = None,
                                    min_amount_products: int = None,
                                    max_amount_products: int = None):
        return self.stores_manager.add_purchase_product_policy(store_id, permitted_user, min_amount_products, max_amount_products)

    def add_purchase_composite_policy(self, store_id: int = None, permitted_user: str = None,
                                      purchase_policies_id = None,
                                      logic_operator: LogicOperator = None):
        return self.add_purchase_composite_policy(store_id, permitted_user, purchase_policies_id, logic_operator)

    def add_policy_to_purchase_composite_policy(self, store_id: int = None, permitted_user: str = None,
                                                composite_id: int = None,
                                                policy_id: int = None):
        return self.stores_manager.add_policy_to_purchase_composite_policy(store_id, permitted_user, composite_id, policy_id)

    def add_product_to_purchase_product_policy(self, store_id: int = None, policy_id: int = None,
                                               permitted_user: str = None,
                                               product_name: str = None):
        return self.stores_manager.add_product_to_purchase_product_policy(store_id, policy_id, permitted_user, product_name)

    def remove_purchase_policy(self, store_id: int = None, permitted_user: str = None, policy_id: int = None):
        return self.stores_manager.remove_purchase_policy(store_id, permitted_user, policy_id)

    def remove_product_from_purchase_product_policy(self, store_id: int = None, policy_id: int = None,
                                                    permitted_user: str = None,
                                                    product_name: str = None):
        return self.stores_manager.remove_product_from_purchase_product_policy(store_id, policy_id, permitted_user, product_name)

    def get_discounts(self, store_id: int = None):
        return self.stores_manager.get_discounts(store_id)

    def get_discount_details(self, store_id: int = None, discount_id: int = None):
        return self.stores_manager.get_discount_details(store_id, discount_id)

    def get_purchases_policies(self, store_id: int = None):
        return self.stores_manager.get_purchases_policies(store_id)

    def get_purchase_policy_details(self, store_id: int = None, purchase_policy_id: int = None):
        return self.stores_manager.get_purchase_by_id(store_id, purchase_policy_id)

    def get_cart_description(self, cart = None):  #NEED_TO_CHECK
        return self.stores_manager.get_cart_description(cart)

    def get_updated_basket(self, basket = None):
        return self.stores_manager.get_updated_basket(basket)

    def add_visible_discount_to_product(self, store_id: int = None, username: str = None, start_date = None,
                                        end_date = None, percent: int = None):
        return self.stores_manager.add_visible_product_discount(store_id, username, start_date, end_date, percent)

    def add_conditional_discount_to_product(self, store_id: int = None, username: str = None, start_date = None,
                                            end_date = None, percent: int = None,
                                            min_amount: int = None, num_prods_to_apply: int = None):
        return self.stores_manager.add_conditional_discount_to_product(store_id, username, start_date, end_date, percent, min_amount, num_prods_to_apply)

    def add_conditional_discount_to_store(self, store_id: int = None, username: str = None, start_date = None,
                                          end_date = None, percent: int = None,
                                          min_price: int = None):
        return self.stores_manager.add_conditional_discount_to_store(store_id, username, start_date, end_date, percent, min_price)

    def add_product_to_discount(self, store_id: int = None, permitted_user: str = None, discount_id: int = None,
                                product_name: str = None):
        return self.stores_manager.add_product_to_discount(store_id, permitted_user, discount_id, product_name)

    def remove_product_from_discount(self, store_id: int = None, permitted_user: str = None,
                                     discount_id: int = None, product_name: str = None):
        return self.stores_manager.remove_product_from_discount(store_id, permitted_user, discount_id, product_name)

    def add_composite_discount(self, store_id: int = None, username: str = None, start_date = None,
                               end_date = None, logic_operator: LogicOperator = None,
                               discounts_products_dict: dict = None, discounts_to_apply_id: list = None):  # discounts_products_dict = {discount_id, [products_names]}
        return self.stores_manager.add_composite_discount(store_id, username, start_date, end_date, logic_operator,
                                                          discounts_products_dict, discounts_to_apply_id)

    def edit_visible_discount_to_product(self, store_id: int = None, username: str = None,
                                         discount_id: int = None, start_date = None, end_date = None,
                                         percent: int = None):
        return self.stores_manager.edit_visible_discount_to_product(store_id, username, discount_id, start_date, end_date, percent)

    def edit_conditional_discount_to_product(self, store_id: int = None, discount_id: int = None, username: str = None,
                                             start_date = None, end_date = None,
                                             percent: int = None, min_amount: int = None, nums_to_apply: int = None):
        return self.stores_manager.edit_conditional_discount_to_product(store_id, discount_id, username, start_date,
                                                                        end_date, percent, min_amount, nums_to_apply)

    def edit_conditional_discount_to_store(self, store_id: int = None, discount_id: int = None, username: str = None,
                                           start_date = None, end_date = None,
                                           percent: int = None,
                                           min_price: int = None):
        return self.edit_conditional_discount_to_store(store_id, discount_id, username, start_date, end_date, percent, min_price)


