from project.domain_layer.users_managment.Basket import Basket


class Cart:
    def __init__(self):
        self.baskets = {}
        #{store_id, basket}

    def add_basket(self, store_id):
        if store_id not in self.baskets.keys():
            basket = Basket(store_id)
            self.baskets[store_id] = basket
            return basket

    def remove_basket(self, store_id):
        if store_id in self.baskets.keys():
            self.baskets.pop(store_id)

    def get_basket(self, store_id):
        if store_id in self.baskets.keys():
            return self.baskets[store_id]
        return None

    def get_total(self):
        total = 0
        for basket in self.baskets.values():
            total += basket.get_total()
        return total

    def view(self):
        return self.baskets

    # def get_total_cart(self):
    #     for basket in self.baskets:


    def remove_product(self, store_id, product, quantity):
        basket = self.get_basket(store_id)
        if basket is not None:
            basket.remove_product(product, quantity)
            if basket.products == {}:
                self.baskets.pop(store_id)
        else:
            return False

    def add_product(self, store_id, product, quantity):
        basket = self.get_basket(store_id)
        if basket is None:
            basket = self.add_basket(store_id)
        basket.add_product(product, quantity)
        return True

    def clear_cart(self):
        self.baskets = {}

