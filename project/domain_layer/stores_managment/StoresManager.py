import logging
from project import logger

from project.domain_layer.external_managment.Purchase import Purchase
from project.domain_layer.stores_managment.DiscountsPolicies.CompositeDiscount import CompositeDiscount
from project.domain_layer.stores_managment.DiscountsPolicies.ConditionalProductDiscount import \
    ConditionalProductDiscount
from project.domain_layer.stores_managment.DiscountsPolicies.ConditionalStoreDiscount import ConditionalStoreDiscount
from project.domain_layer.stores_managment.DiscountsPolicies.DiscountPolicy import Discount
from project.domain_layer.stores_managment.DiscountsPolicies.LogicOperator import LogicOperator
from project.domain_layer.stores_managment.DiscountsPolicies.VisibleProductDiscount import VisibleProductDiscount
from project.domain_layer.stores_managment.NullStore import NullStore
from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.PurchasesPolicies import PurchasePolicy
from project.domain_layer.stores_managment.Store import Store
from project.domain_layer.users_managment import Basket
from project.domain_layer.users_managment.Cart import Cart
from project.domain_layer.communication_managment.Publisher import Publisher

import json


def get_logic_operator(logic_operator_str: str):
    if logic_operator_str is None:
        return None
    if logic_operator_str.upper() == "OR":
        return LogicOperator.OR
    elif logic_operator_str.upper() == "AND":
        return LogicOperator.AND
    elif logic_operator_str.upper() == "XOR":
        return LogicOperator.XOR
    else:
        return None


class StoresManager:
    def __init__(self):
        self.publisher = None
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

# TODO: ask Amit if search result include store id?
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
            if store_id is None:
                logger.error("store is none")
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

# TODO: add Publisher
    def add_purchase_to_store(self, store_id: int, purchase: Purchase):
        return self.get_store(store_id).add_new_sale(purchase)

    def open_store(self, owner: str, store_name):
        self.stores[self.stores_idx] = Store(self.stores_idx, store_name, owner)
        self.stores_idx += 1
        return self.stores_idx - 1

    def buy(self, cart: Cart):
        if not self.check_cart_validity(cart):
            return False

        price, description = self.get_cart_description(cart)

        #  if user dont have enough money according to 'price' will return false

        #  user will also get a description for his purchase

        for store in cart.baskets.keys():
            basket = cart.get_basket(store)
            for product in basket.products.keys():
                if not self.get_store(store).buy_product(product, basket.products.get(product)[1]):
                    return False
            self.get_store(basket.store_id).sales.append(description[basket.store_id])
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

    def add_visible_product_discount(self, store_id: int, username: str, start_date, end_date, percent: int):
        store = self.get_store(store_id)
        return store.add_visible_product_discount(username,
                                                     VisibleProductDiscount(start_date, end_date, percent))

    def add_conditional_discount_to_product(self, store_id: int, username: str, start_date, end_date, percent: int, min_amount: int, num_prods_to_apply: int):
        store = self.get_store(store_id)
        return store.add_conditional_discount_to_product(username,
                                                     ConditionalProductDiscount(start_date, end_date, percent, min_amount, num_prods_to_apply))

    def add_conditional_discount_to_store(self, store_id: int, username: str, start_date, end_date, percent: int, min_price: int):
        store = self.get_store(store_id)
        return store.add_conditional_discount_to_store(username,
                                                       ConditionalStoreDiscount(start_date, end_date, percent, min_price))

    def add_product_to_discount(self, store_id: int, permitted_user: str, discount_id: int, product_name):
        store = self.get_store(store_id)
        return store.add_product_to_discount(permitted_user, discount_id, product_name)

    def remove_product_from_discount(self, store_id: int, permitted_user: str, discount_id: int, product_name):
        store = self.get_store(store_id)
        return store.remove_product_from_discount(permitted_user, discount_id, product_name)

    def add_composite_discount(self, store_id: int, username: str, start_date, end_date, logic_operator_str: str, discounts_products_dict: dict, discounts_to_apply_id: list):
        store = self.get_store(store_id)  #                                                                                {dicount_id, [product_names]}
        tup_list = []
        discounts_to_apply_list = []
        logic_operator: LogicOperator = get_logic_operator(logic_operator_str)

        for discount_id in discounts_products_dict.keys():
            if discount_id not in store.discounts.keys():
                return False
            discount: Discount = store.discounts[discount_id]
            products_to_check_list = discounts_products_dict[discount_id]
            tup_list.append((discount, products_to_check_list))  # (Discount, (products_names))

        for discount_id in discounts_to_apply_id:
            if discount_id not in store.discounts.keys():
                return False
            discount = store.discounts[discount_id]
            discounts_to_apply_list.append(discount)

        return store.add_composite_discount(username,
                                                       CompositeDiscount(start_date, end_date, logic_operator, tup_list, discounts_to_apply_list))

    def edit_visible_discount_to_product(self, store_id: int, username: str, discount_id:int, start_date, end_date, percent: int):
        store = self.get_store(store_id)
        return store.edit_visible_discount(username, discount_id, start_date, end_date, percent)

    def edit_conditional_discount_to_product(self, store_id: int, discount_id: int, username: str, start_date, end_date, percent: int,
                                             min_amount: int, nums_to_apply: int):
        store = self.get_store(store_id)
        return store.edit_conditional_discount_to_product(username, discount_id, start_date, end_date, percent, min_amount, nums_to_apply)

    def edit_conditional_discount_to_store(self, store_id: int, discount_id: int, username: str, start_date, end_date, percent: int,
                                             min_price: int):
        store = self.get_store(store_id)
        return store.edit_conditional_discount_to_store(username, discount_id, start_date, end_date, percent, min_price)

    def remove_manager(self, store_id, owner, to_remove):
        store = self.get_store(store_id)
        return store.remove_manager(owner, to_remove)

    def remove_owner(self, store_id, owner, to_remove):
        store = self.get_store(store_id)
        return store.remove_owner(owner, to_remove)

    def add_purchase_store_policy(self, store_id: int, permitted_user: str, min_amount_products: int, max_amount_products: int):
        store = self.get_store(store_id)
        return store.add_purchase_store_policy(permitted_user, min_amount_products, max_amount_products)

    def add_purchase_product_policy(self, store_id: int, permitted_user: str, min_amount_products: int, max_amount_products: int):
        store = self.get_store(store_id)
        return store.add_purchase_product_policy(permitted_user, min_amount_products, max_amount_products)

    def add_purchase_composite_policy(self, store_id: int, permitted_user: str, purchase_policies_id, logic_operator_str: str):
        logic_operator = get_logic_operator(logic_operator_str)
        if purchase_policies_id is None or logic_operator is None:
            return False, "The parameters are not valid"

        store = self.get_store(store_id)
        policies = []

        for purch_policy_id in purchase_policies_id:
            if purch_policy_id not in store.purchase_policies.keys():
                return False, "Wrong policy id was inserted \n"
            policy: PurchasePolicy = store.purchase_policies[purch_policy_id]
            policies.append(policy)

        return store.add_purchase_composite_policy(permitted_user, policies, logic_operator)

    def add_policy_to_purchase_composite_policy(self, store_id: int, permitted_user: str, composite_id: int, policy_id: int):
        store = self.get_store(store_id)
        return store.add_policy_to_purchase_composite_policy(permitted_user, composite_id, policy_id)

    def add_product_to_purchase_product_policy(self, store_id: int, policy_id: int, permitted_user: str, product_name: str):
        store = self.get_store(store_id)
        return store.add_product_to_purchase_product_policy(policy_id, permitted_user, product_name)

    def remove_purchase_policy(self, store_id: int, permitted_user: str, policy_id):
        store = self.get_store(store_id)
        return store.remove_purchase_policy(policy_id, permitted_user)

    def remove_product_from_purchase_product_policy(self, store_id: int, policy_id: int, permitted_user: str, product_name: str):
        store = self.get_store(store_id)
        return store.remove_product_from_purchase_product_policy(policy_id, permitted_user, product_name)

    def get_discounts(self, store_id):
        store = self.get_store(store_id)
        description = store.get_discounts()
        return description

    def get_discount_details(self, store_id: int, discount_id: int):
        store = self.get_store(store_id)
        return store.get_discount_by_id(discount_id)

    def get_purchases_policies(self, store_id):
        store = self.get_store(store_id)
        return store.get_purchase_policies()

    def get_purchase_by_id(self, store_id: int, purchase_policy_id: int):
        store = self.get_store(store_id)
        return store.get_purchase_policy_by_id(purchase_policy_id)

    def check_cart_validity(self, cart: Cart):
        baskets = cart.baskets

        is_approved = True
        description = ""

        for basket in baskets.values():
            store = self.get_store(basket.store_id)
            description += "\n" + store.name + "\n"
            p_approved, outcome = store.check_basket_validity(basket)

            if not p_approved:
                description += outcome
                is_approved = False

        return is_approved, description

    def get_cart_description(self, cart: Cart):
        baskets = cart.baskets
        cart_price = 0
        cart_discription_dict = {}

        for basket in baskets.values():
            updated_dict_basket = self.get_updated_basket(basket)
            cart_price += self.get_total_basket_price(updated_dict_basket)
            cart_discription_dict[basket.store_id] = (self.get_basket_description(updated_dict_basket.values()))

        return cart_price, cart_discription_dict

    def get_updated_basket(self, basket: Basket):
        store = self.get_store(basket.store_id)
        return store.get_updated_basket(basket)  # {product_name, (Product, amount, updated_price, policy)}

    def get_total_basket_price(self, updated_basket_dict):
        price = 0.0
        for product in updated_basket_dict.values():
            price += float(product[2])
        return price

    def get_basket_description(self, product_tup_list):
        basket_dict = {}
        for product_tup in product_tup_list:
            basket_dict[product_tup[0].name] = [product_tup[1], product_tup[2], product_tup[3]]
        return basket_dict

    def get_stores_description(self):
        stores_description = {}  #  {store_name: [store_details]}
        for store in self.stores.values():
            stores_description[store.name] = store.get_description()
        return stores_description

    def get_inventory_description(self, store_id: int):
        store = self.get_store(store_id)
        description = store.get_inventory_description()
        return description

    def get_store_description_by_id(self, store_id):
        store = self.get_store(store_id)
        description = store.get_description()
        return description

    def get_jsn_description(self, store_id):
        store = self.get_store(store_id)
        jsn_desc = store.get_jsn_description()
        return json.dumps(jsn_desc)

   def bound_publisher(self, publisher: Publisher):
        self.publisher = publisher

# TODO: implement - this method get store id, product name (name is unique? if not, we might have a problem..)
    #  TODO: and returns the product.
    def get_product_from_store(self, store_id, product_name):
        pass
