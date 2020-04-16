class Proxy:

    def __init__(self):
        self.real = None
        self.out = True
        # adapter = Adapter()
        self.remove = False
        self.update = False
        self.appoint = False
    # def set_real(self, adapter):
    # self.real = Adapter()

    def register(self, username, password):
        if self.real != None:
            self.real.register(username, password)
        else:
            return True

    def login(self, username, password):
        if self.real is not None:
            self.real.login(username, password)
        else:
            self.out = False
            if username == "userNotName":
                return False
            else:
                return True

    def showProductStore(self, store):
        if self.real != None:
            self.real.showProductStore(store)
        else:
            return True

    def add_Store(self, StoreName, StoreId):
        if self.real != None:
            self.real.add_Store(self, StoreName, StoreId)
        else:
            return True

    def add_product_to_Store(self, StoreID, product_name: str, product_price: int,
                             product_categories: [str],
                             key_words: [str], amount):
        if self.real != None:
            self.real.add_product_to_Store(self, StoreID)
        else:
            if StoreID >= 40:
                return False
            if self.out:
                return False
            return True

    def searchProduct(self, product, category=None, key_words=None):
        if self.real != None:
            self.real.searchProduct(self, product, category, key_words)
        else:
            product_type = type('Product', (object,), {})
            if not self.update:

                p = product_type()
                p.name = "Banana"
                p.price = 20
                p.categories = ["Food"]
                p.key_words = ["Fruits"]
                p.amount = 10
                if not self.remove:
                    return {0: [p]}
                else:
                    return {1: [p]}
            else:

                p = product_type()
                p.name = "Banana"
                p.price = 40
                p.categories = ["yellow", "Food"]
                p.key_words = ["Fruits"]
                p.amount = 40
                if not self.remove:
                    return {0: [p]}
                else:
                    return {1: [p]}

    def Open_store(self, store_name):
        if self.real != None:
            self.real.Open_store(self, store_name)
        else:
            if store_name == "Failed": return -1
            return 0

    def get_managed_stores(self):
        if self.real != None:
            self.real.get_managed_stores(self)
        else:
            return [0]

    def logout(self):
        if self.real != None:
            self.real.logout(self)
        else:
            self.out = True
            return True

    def get_purchase_history(self):
        if self.real != None:
            return self.real.get_purchase_history()
        else:
            purchase_type = type('Purchase', (object,), {})
            product_type = type('Product', (object,), {})
            p = product_type()
            p.name = "Banana"
            pur = purchase_type()
            pur.products = [p]
            return pur

    def add_product(self, store_id, product, amount):
        if self.real != None:
            return self.real.add_product(store_id, product, amount)
        else:

            return True

    def buy(self):
        if self.real != None:
            return self.real.buy()
        else:
            return True

    def remove_product_from_store(self, store_id, product_name):
        if self.real != None:
            return self.real.remove_product_from_store(store_id, product_name)
        else:
            self.remove = True
            if self.out:
                return False
            if store_id >= 40:
                return False
            return True

    def update_product(self, store_id, product_name, att, updated):
        if self.real != None:
            return self.real.update_product(store_id, product_name, att, updated)
        else:
            if updated is int and updated < 0:
                return False
            if product_name != "Banana":
                return False
            self.update = True
            if store_id >= 40:
                return False
            if self.out:
                return False
            return True

    def add_new_store_owner(self, user,store_id):
        if self.real != None:
            return self.real.add_new_store_owner(user,store_id)
        else:
            if self.appoint:
                self.appoint = not self.appoint
                return False

            if self.out:
                return False
            if user == "not new owner":
                return False
            if store_id>=40:
                return False
            self.appoint = not self.appoint
            return True

    def add_new_store_manager(self, user, store_id):
        if self.real != None:
            return self.real.add_new_store_owner(user, store_id)
        else:
            if self.appoint:
                self.appoint = not self.appoint
                return False

            if self.out:
                return False
            if user == "not new manager":
                return False
            if store_id >= 40:
                return False
            self.appoint = not self.appoint
            return True
