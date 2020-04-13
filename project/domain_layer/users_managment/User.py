from project.domain_layer.users_managment.Cart import Cart


class User:
    def __init__(self, name):
        self.cart = Cart()
        self.username = name
        self.purchase_history = []

    def view_cart(self):
        self.cart.view()

    def remove_product(self, store_id, product, quantity):
        self.cart.remove_product(store_id, product, quantity)

    def add_product(self, store_id, product, quantity):
        self.cart.add_product(store_id, product, quantity)
        return True

    def get_cart(self):
        return self.cart

    def remove_cart(self):
        self.cart = {}

    def add_purchase(self, purchase):
        self.purchase_history.append(purchase)


