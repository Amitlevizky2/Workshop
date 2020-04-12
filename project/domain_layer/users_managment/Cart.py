from project.domain_layer.users_managment.Basket import Basket


class Cart:
    def __init__(self):
        self.baskets = {}
        #{store_id, basket}

    def add_basket(self, store_id):
        if self.baskets[store_id] is None:
            return Basket(store_id)

    def remove_basket(self, store_id):
        if self.baskets[store_id] is not None:
            self.baskets.pop(store_id)

    def get_basket(self, store_id):
        return self.baskets[store_id]

    def get_total(self):
        total = 0
        for basket in self.baskets:
            total += basket.get_total()

    def view(self):
        return self.baskets
