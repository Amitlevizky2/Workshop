from project.domain_layer.users_managment.RegisteredUser import RegisteredUser


class NullUser(RegisteredUser):

    def __init__(self):
        super(NullUser, self).__init__("null")

    def view_purchase_history(self):
        return None

    def logout(self):
        return False

    def login(self):
        return False

    def view_cart(self):
        return None

    def remove_product(self, store, product, quantity):
        return False

    def add_product(self, store, product, quantity):
        return False

    def get_cart(self):
        return None

    def get_managed_store(self):
        return None

    def add_managed_store(self, store_id):
        return False

    def remove_cart(self):
        return None

    def add_purchase(self, purchase):
        return False
