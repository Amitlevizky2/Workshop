from project.domain_layer.stores_managment.Inventory import Inventory
from project.domain_layer.stores_managment.Product import Product
from project.domain_layer.users_managment import User


class Store():
    def __init__(self, store_id, name, store_owner):
        self.id = store_id
        self.name = name
        self.inventory = Inventory()
        self.sale_policy = None
        self.discount_policy = None
        self.store_owners = [store_owner]
        self.rate = 0

    def add_product(self, user: User, product_name: str, product_price: int, product_category, key_words: list) -> bool:
        if user in self.store_owners:
            self.inventory.add_product(Product(product_name, product_price, product_category, key_words))
            return True
        else:
            return False
