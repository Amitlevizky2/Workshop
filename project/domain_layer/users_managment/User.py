from project.domain_layer.users_managment.Cart import Cart


class User:
    def __init__(self, name):
        self.cart = Cart()
        self.username = name
        self.purchase_history = []

    def view_cart(self):
        self.cart.view()
