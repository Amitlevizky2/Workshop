from project.domain_layer.external_managment.Purchase import Purchase
from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.Store import Store


class NullStore(Store):
    def __init__(self):
        pass

    def appoint_owner(self, owner, to_appoint):
        return False

    def remove_owner(self, owner, to_remove):
        return False

    def remove_manager(self, owner, to_remove):
        return False

    def add_permission_to_manager(self, owner, manager, permission):
        return False

    def remove_permission_from_manager(self, owner, manager, permission):
        return False

    def appoint_manager(self, owner, to_appoint):
        return False

    def add_product(self, user_name: str, product_name: str, product_price: int, product_categories, key_words: [str],
                    amount) -> bool:
        return False

    def search(self, search_term: str = "", categories: [str] = None, key_words: [str] = None) -> [Product]:
        return False

    def buy_product(self, product_name, amount):
        return False

    def get_sales_history(self, user, is_admin) -> [Purchase]:
        return False

    def update_product(self, user, product_name, attribute, updated):
        return False

    def add_new_sale(self, purchase: Purchase) -> bool:
        return False

    def check_permission(self, user, function):
        return False
