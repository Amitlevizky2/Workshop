from datetime import datetime

from project.data_access_layer.PurchaseORM import PurchaseORM
from project.domain_layer.stores_managment.Product import Product


class Purchase:
    def __init__(self, products, buyer_name, store_id, purchase_id, orm):
        self.buyer = buyer_name
        self.store_id = store_id
        self.products = products
        self.purchase_id = purchase_id
        self.date = datetime.now()
        if orm is None:
            self.orm = PurchaseORM()
            self.orm.username = buyer_name
            self.orm.store_id = store_id
            self.orm.date = self.date
            self.orm.add()
        else:
            self.orm = orm

