from project.domain_layer.external_managment.Purchase import Purchase
from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.stores_managment.Store import Store


class NullStore(Store):
    def __init__(self):
        pass

    def appoint_owner(self, owner, to_appoint):
        pass

    def remove_owner(self, owner, to_remove):
        pass

    def remove_manager(self, owner, to_remove):
        pass

    def add_permission_to_manager(self, owner, manager, permission):
        pass

    def remove_permission_from_manager(self, owner, manager, permission):
        pass

    def appoint_manager(self, owner, to_appoint):
        pass

    def add_product(self, user_name: str, product_name: str, product_price: int, product_categories, key_words: [str],
                    amount) -> bool:
        pass

    def search(self, search_term: str = "", categories: [str] = None, key_words: [str] = None) -> [Product]:
        pass

    def buy_product(self, product_name, amount):
        pass

    def get_sales_history(self, user, is_admin) -> [Purchase]:
        pass

    def update_product(self, user, product_name, attribute, updated):
        pass

    def add_new_sale(self, purchase: Purchase) -> bool:
        pass

    def check_permission(self, user, function):
        pass
