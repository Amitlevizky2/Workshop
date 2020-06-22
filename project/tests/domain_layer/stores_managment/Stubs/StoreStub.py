import datetime

from project.domain_layer.communication_managment.Publisher import Publisher
from project.domain_layer.external_managment.Purchase import Purchase
from project.domain_layer.stores_managment.DiscountsPolicies.DiscountPolicy import Discount
from project.domain_layer.stores_managment.DiscountsPolicies.LogicOperator import LogicOperator
from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.PurchasesPolicies.PurchaseProductPolicy import PurchaseProductPolicy
from project.domain_layer.stores_managment.Store import Store

class StoreStub(Store):

    def __init__(self, store_id, name, store_owner):
        super().__init__(store_id, name, store_owner)
        # self.init_discount()
        # self.init_purchase_policy()
        # self.init_inventory()

    def appoint_owner(self, owner, to_appoint):
        if owner is 'store_owner11' and to_appoint is 'owner':
            return {'error': False,
                    'error_msg': 'succesfully added'}

        else:
            return {'error': True,
                    'error_msg': 'wrong'}

    def appoint_owner_helper(self, owner, to_appoint):
        return super().appoint_owner_helper(owner, to_appoint)

    def remove_owner(self, owner, to_remove, publisher: Publisher):
        if owner is 'store_owner11' and to_remove is 'to_remove':
            return {'error': False,
                    'error_msg': 'succesfully added'}

        else:
            return {'error': True,
                    'error_msg': 'wrong'}

    def remove_manager(self, owner, to_remove):
        if owner is 'store_owner11' and to_remove is 'manager':
            return {'error': False,
                    'error_msg': 'succesfully added'}

        else:
            return {'error': True,
                    'error_msg': 'wrong'}

    def add_permission_to_manager(self, owner, manager, permission):
        if owner is 'store_owner11' and manager is 'manager' and permission is 'add_product':
            return {'error': False,
                    'error_msg': 'succesfully added'}

        else:
            return {'error': True,
                    'error_msg': 'wrong'}

    def remove_permission_from_manager(self, owner, manager, permission):
        if owner is 'store_owner11' and manager is 'manager' and permission is 'add_product':
            return {'error': False,
                    'error_msg': 'succesfully added'}

        else:
            return {'error': True,
                    'error_msg': 'wrong'}

    def appoint_manager(self, owner, to_appoint):
        if owner is 'store_owner11' and to_appoint is 'manager':
            return {'error': False,
                    'error_msg': 'succesfully added'}

        else:
            return {'error': True,
                    'error_msg': 'wrong'}

    def add_product(self, user_name: str, product_name: str, product_price: int, product_categories, key_words: [str],
                    amount):
        return super().add_product(user_name, product_name, product_price, product_categories, key_words, amount)

    def search(self, search_term: str = "", categories=[], key_words=[]) -> [Product]:
        return 'Banana'

    def products_after_discount(self, result):
        super().products_after_discount(result)

    def buy_product(self, product_name, amount):
        return super().buy_product(product_name, amount)

    def get_sales_history(self, user, is_admin) -> [Purchase]:
        return super().get_sales_history(user, is_admin)

    def update_product(self, user, product_name, attribute, updated):
        return super().update_product(user, product_name, attribute, updated)

    def add_new_sale(self, purchase: Purchase, publisher: Publisher):
        return super().add_new_sale(purchase, publisher)

    def check_permission(self, user, function):
        return super().check_permission(user, function)

    def get_store_products(self):
        return super().get_store_products()

    def remove_product(self, product_name, username):
        if username is 'store_owner11' and product_name is 'Banana':
            return {'error': False,
                    'error_msg': 'succesfully added'}

        else:
            return {'error': True,
                    'error_msg': 'wrong'}

    def add_visible_product_discount(self, permitted_username, discount: Discount):
        return super().add_visible_product_discount(permitted_username, discount)

    def add_conditional_discount_to_product(self, permitted_username, discount):
        return super().add_conditional_discount_to_product(permitted_username, discount)

    def add_conditional_discount_to_store(self, permitted_username, discount):
        return super().add_conditional_discount_to_store(permitted_username, discount)

    def add_composite_discount(self, permitted_username: str, discount: Discount):
        if permitted_username is 'store_owner11' and discount.logic_operator == LogicOperator.AND:
            return {'error': False,
                    'error_msg': 'succesfully added'}

        else:
            return {'error': True,
                    'error_msg': 'wrong'}

    def edit_visible_discount(self, permitted_username, discount_id, start_date, end_date, percent):
        return super().edit_visible_discount(permitted_username, discount_id, start_date, end_date, percent)

    def edit_conditional_discount_to_product(self, permitted_username: str, discount_id: int, start_date, end_date,
                                             percent, min_amount: int, nums_to_apply: int):
        return super().edit_conditional_discount_to_product(permitted_username, discount_id, start_date, end_date,
                                                            percent, min_amount, nums_to_apply)

    def edit_conditional_discount_to_store(self, permitted_username: str, discount_id: int, start_date, end_date,
                                           percent: int, min_price: int):
        return super().edit_conditional_discount_to_store(permitted_username, discount_id, start_date, end_date,
                                                          percent, min_price)

    def is_owner(self, username):
        return super().is_owner(username)

    def add_product_to_discount(self, permitted_user: str, discount_id: int, product_name: str):
        if permitted_user is 'store_owner11' and discount_id is 1 and product_name is 'Banana':
            return {'error': False,
                    'error_msg': 'succesfully added'}

        else:
            return {'error': True,
                    'error_msg': 'wrong'}

    def remove_product_from_discount(self, permitted_user, discount_id, product_name):
        if permitted_user is 'store_owner11' and discount_id is 1 and product_name is 'Banana':
            return {'error': False,
                    'error_msg': 'succesfully added'}

        else:
            return {'error': True,
                    'error_msg': 'wrong'}

    def add_purchase_store_policy(self, permitted_user, min_amount_products, max_amount_products):
        return super().add_purchase_store_policy(permitted_user, min_amount_products, max_amount_products)

    def add_purchase_product_policy(self, permitted_user, min_amount_products, max_amount_products):
        return super().add_purchase_product_policy(permitted_user, min_amount_products, max_amount_products)

    def add_purchase_composite_policy(self, permitted_user: str, policies: list, logic_operator: LogicOperator):
        return super().add_purchase_composite_policy(permitted_user, policies, logic_operator)

    def add_policy_to_purchase_composite_policy(self, permitted_user: str, composite_id, policy_id: int):
        return super().add_policy_to_purchase_composite_policy(permitted_user, composite_id, policy_id)

    def add_product_to_purchase_product_policy(self, policy_id, permitted_user: str, product_name: str):

        return super().add_product_to_purchase_product_policy(policy_id, permitted_user, product_name)

    def remove_product_from_purchase_product_policy(self, policy_id, permitted_user, product_name):
        return super().remove_product_from_purchase_product_policy(policy_id, permitted_user, product_name)

    def get_discounts(self):
        return super().get_discounts()

    def get_discount_by_id(self, discount_id):
        return super().get_discount_by_id(discount_id)

    def get_purchase_policies(self):
        return super().get_purchase_policies()

    def get_purchase_policy_by_id(self, purchase_policy_id: int):
        return super().get_purchase_policy_by_id(purchase_policy_id)

    def check_basket_validity(self, basket):
        return super().check_basket_validity(basket)

    def remove_purchase_policy(self, policy_id, permitted_user):
        return super().remove_purchase_policy(policy_id, permitted_user)

    def get_description(self):
        return super().get_description()

    def get_inventory_description(self):
        return super().get_inventory_description()

    def get_product(self, product_name):
        return super().get_product(product_name)

    def get_store_managers(self):
        return super().get_store_managers()

    def get_user_permissions(self, username):
        if username is 'store_owner11':
            return {'error': False,
                    'error_msg': 'succesfully added'}

        else:
            return {'error': True,
                    'error_msg': 'wrong'}

    def get_all_permissions(self):
        return super().get_all_permissions()

    def is_valid_amount(self, product_name, quantity):
        if product_name is 'Banana' and quantity > 11:
            return {'error': False,
                    'error_msg': 'succesfully added'}

        else:
            return {'error': True,
                    'error_msg': 'wrong'}

    def init_discount(self):
        from project.domain_layer.stores_managment.DiscountsPolicies.VisibleProductDiscount import \
            VisibleProductDiscount
        vis_discount = VisibleProductDiscount(datetime.datetime(2018, 6, 1), datetime.datetime(2020, 12, 17), 5, 1)
        # cond_discount = ConditionalProductDiscount(datetime.datetime(2018, 6, 1), datetime.datetime(2020, 12, 17), 5, 2, 2)
        self.discounts[1] = vis_discount

    def init_inventory(self):
        pass

    def init_purchase_policy(self):
        policy = PurchaseProductPolicy(2, 6, 1, 1)
        self.purchase_policies[1] = policy
