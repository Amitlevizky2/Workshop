import jsons

from project.domain_layer.users_managment.Cart import Cart


class User:
    def __init__(self, name):
        self.cart = Cart()
        self.username = name
        self.purchase_history = []

    def view_cart(self):
        self.cart.view()

    # TODO: change argument product to product_name
    def remove_product(self, store_id, product, quantity) -> bool:
        return self.cart.remove_product(store_id, product, quantity)

    def add_product(self, store_id, product, quantity):
        self.cart.add_product(store_id, product, quantity)
        return True

    def get_cart(self, view_format=''):
        if view_format == 'json':
            return self.cart.get_jsn_description()
        return self.cart

    def remove_cart(self):
        self.cart.clear_cart()

    def add_purchase(self, purchase):
        self.purchase_history.append(purchase)

    def view_purchase_history(self):
        return self.purchase_history

    def get_jsn_description(self):
        json_cart = self.cart.get_jsn_description()
        json_purchase_history = self.get_jsn_purchase_history()
        return jsons.dumps({
            'username': self.username,
            'cart': json_cart,
            'purchase_history': json_purchase_history
        })

    def get_jsn_purchase_history(self):
        return []

    def merge_carts(self, other: Cart):
        self.cart.merge_carts(other)



