from project.domain_layer.external_managment.Purchase import Purchase
from project.domain_layer.stores_managment.DiscountsPolicies.DiscountPolicy import Discount
from project.domain_layer.stores_managment.DiscountsPolicies.LogicOperator import LogicOperator
from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.Store import Store
from project.domain_layer.users_managment import Basket


class NullStore(Store):
    def __init__(self):
        pass

    def appoint_owner(self, owner, to_appoint):
        return {'ans': False,
                'desc': "The store id is not exist"}

    def remove_owner(self, owner, to_remove):
        return {'ans': False,
                'desc': "The store id is not exist"}

    def remove_manager(self, owner, to_remove):
        return {'ans': False,
                'desc': "The store id is not exist"}

    def add_permission_to_manager(self, owner, manager, permission):
        return {'ans': False,
                'desc': "The store id is not exist"}

    def remove_permission_from_manager(self, owner, manager, permission):
        return {'ans': False,
                'desc': "The store id is not exist"}

    def appoint_manager(self, owner, to_appoint):
        return {'ans': False,
                'desc': "The store id is not exist"}

    def add_product(self, user_name: str, product_name: str, product_price: int, product_categories, key_words: [str],
                    amount) -> bool:
        return {'ans': False,
                'desc': "The store id is not exist"}

    def search(self, search_term: str = "", categories: [str] = None, key_words: [str] = None) -> [Product]:
                return {'ans': False,
                'desc': "The store id is not exist"}

    def buy_product(self, product_name, amount):
                return {'ans': False,
                'desc': "The store id is not exist"}

    def get_sales_history(self, user, is_admin) -> [Purchase]:
        return []

    def update_product(self, user, product_name, attribute, updated):
                return {'ans': False,
                'desc': "The store id is not exist"}

    def add_new_sale(self, purchase: Purchase) -> bool:
                return {'ans': False,
                'desc': "The store id is not exist"}


    def add_visible_discount_to_product(self, product_name, username, discount):
                return {'ans': False,
                'desc': "The store id is not exist"}

    def appoint_owner_helper(self, owner, to_appoint):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def check_permission(self, user, function):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def get_store_products(self):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def remove_product(self, product_name, username):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def add_visible_product_discount(self, permitted_username, discount: Discount):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def add_conditional_discount_to_product(self, permitted_username, discount):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def add_conditional_discount_to_store(self, permitted_username, discount):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def add_composite_discount(self, permitted_username: str, discount: Discount):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def edit_visible_discount(self, permitted_username, discount_id, start_date, end_date, percent):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def edit_conditional_discount_to_product(self, permitted_username: str, discount_id: int, start_date, end_date,
                                             percent, min_amount: int, nums_to_apply: int):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def edit_conditional_discount_to_store(self, permitted_username: str, discount_id: int, start_date, end_date,
                                           percent: int, min_price: int):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def is_owner(self, username):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def get_updated_basket(self, basket: Basket):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def add_product_to_discount(self, permitted_user: str, discount_id: int, product_name: str):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def remove_product_from_discount(self, permitted_user, discount_id, product_name):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def add_purchase_store_policy(self, permitted_user, min_amount_products, max_amount_products):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def add_purchase_product_policy(self, permitted_user, min_amount_products, max_amount_products):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def add_purchase_composite_policy(self, permitted_user: str, policies: list, logic_operator: LogicOperator):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def add_policy_to_purchase_composite_policy(self, permitted_user: str, composite_id, policy_id: int):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def add_product_to_purchase_product_policy(self, policy_id, permitted_user: str, product_name: str):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def remove_product_from_purchase_product_policy(self, policy_id, permitted_user, product_name):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def get_discounts(self):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def get_discount_by_id(self, discount_id):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def get_purchase_policies(self):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def get_purchase_policy_by_id(self, purchase_policy_id: int):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def check_basket_validity(self, basket: Basket):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

    def remove_purchase_policy(self, policy_id, permitted_user):
                return {'ans': False,
                'desc': "The store id is not exist"}, "Store id not exist"

