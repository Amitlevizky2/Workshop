from project.domain_layer.stores_managment.Inventory import Inventory
from project.domain_layer.stores_managment.Product import Product


class Store():
    def __init__(self, id, name, store_owner):
        self.id = id
        self.name = name
        self.inventory = Inventory()
        self.sale_policy = None
        self.discount_policy = None
        self.store_owners = [store_owner]
        self.rate = 0

    def search(self, search_term: str = "", categories: [str] = None, key_words: [str] = None) -> [Product]:
        result = []
        for product_name in self.inventory.products.keys():
            if search_term in product_name:
                result.append(self.inventory.products.get(product_name)[0])
        if categories is not None:
            for product in result:
                for category in categories:
                    if category not in product.categories:
                        result.remove(product)

        if key_words is not None:
            for product in result:
                for word in key_words:
                    if word not in product.key_words:
                        result.remove(product)
        return result