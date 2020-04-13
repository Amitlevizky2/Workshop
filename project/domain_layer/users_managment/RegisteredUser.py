from project.domain_layer.users_managment.User import User


class RegisteredUser(User):

    def __init__(self, username):
        super().__init__()
        self.username = username
        self.purchase_history = []
        self.loggedin = False
        self.managed_stores = []

    def logout(self):
        self.loggedin = False

    def login(self):
        self.loggedin = True

    def view_purchase_history(self):
        return self.purchase_history

    def get_managed_store(self):
        return self.managed_stores

    def add_managed_store(self, store_id):
        if store_id not in self.managed_stores:
            self.managed_stores.append(store_id)