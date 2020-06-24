from datetime import datetime

import jsons


from project.domain_layer.stores_managment.Product import Product


class Purchase:
    def __init__(self, products, buyer_name, store_id, purchase_id, orm=None):
        self.buyer = buyer_name
        self.store_id = store_id
        self.products = products #{}
        self.purchase_id = purchase_id
        self.date = datetime.now()
        self.order_number = 0
        self.supply_number = 0
        if orm is None:
            from project.data_access_layer.PurchaseORM import PurchaseORM
            self.orm = PurchaseORM()
            self.orm.username = buyer_name
            self.orm.id = purchase_id
            self.orm.store_id = store_id
            self.orm.date = self.date
            self.orm.products = jsons.dumps(products)
            self.orm.add()
        else:
            self.orm = orm

    def set_order_number(self, number: int):
        self.order_number = number

    def set_supply_number(self, number: int):
        self.supply_number = number