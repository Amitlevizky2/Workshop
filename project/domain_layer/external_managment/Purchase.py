from project.domain_layer.stores_managment.Product import Product


class Purchase:
    def __init__(self, products: [Product], buyer_name, store_id):
        self.buyer = buyer_name
        self.store_id = store_id
        self.products = products
