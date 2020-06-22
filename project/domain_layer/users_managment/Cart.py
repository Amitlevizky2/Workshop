from project.domain_layer.users_managment.Basket import Basket


class Cart:
    def __init__(self):
        self.baskets = {}
        #{store_id, basket}

    def add_basket(self, username, store_id):
        if store_id not in self.baskets.keys():
            basket = Basket(username, store_id)
            self.baskets[store_id] = basket
            return basket

    def remove_basket(self, store_id):
        if store_id in self.baskets.keys():
            self.baskets.pop(store_id)

    def get_basket(self, store_id):
        if store_id in self.baskets.keys():
            return self.baskets[store_id]
        return None

    def view(self):
        return self.baskets

# TODO: remove product receive actual product. change to product_name
    def remove_product(self, store_id, product, quantity) -> bool:
        basket = self.get_basket(store_id)
        if basket is not None:
            removed = basket.remove_product(product, quantity)
            if basket.products == {}:
                self.baskets.pop(store_id)
            return removed
        else:
            return False

    def add_product(self, username, store_id, product, quantity) -> bool:
        basket = self.get_basket(store_id)
        if basket is None:
            basket = self.add_basket(username, store_id)
        basket.add_product(product, quantity)
        return True

    def clear_cart(self):
        self.baskets = {}

    def merge_carts(self, other):
        pass

    def get_jsn_description(self):
        """
        :return: cart =
        {
            baskets:
            [
                basket1 (json),
                basket2 (json)
                ...
                basketN (json)
            ]

        }
        """
        baskets_description = []
        for value in self.baskets.values():
            print(type(value))
            baskets_description.append(
                value.get_jsn_description()
            )
        return {
            'baskets': baskets_description
        }
