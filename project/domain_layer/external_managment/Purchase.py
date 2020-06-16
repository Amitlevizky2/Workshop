from datetime import datetime

from project.domain_layer.stores_managment.Product import Product


class Purchase:
    def __init__(self, products, buyer_name, store_id, purchase_id):
        self.buyer = buyer_name
        self.store_id = store_id
        self.products = products
        self.purchase_id = purchase_id
        self.date = datetime.now()
