


class Proxy:

    def __init__(self):
        self.real = None
        # adapter = Adapter()

    # def set_real(self, adapter):
    # self.real = Adapter()
    def add_guest_user(self):
        if self.real != None:
            self.real.add_guest_user()
        else:
            return "guestuser"

    def register(self, username, password):
        if self.real != None:
            self.real.register(username, password)
        else:
            return True

    def login(self, username, password):
        if self.real is not None:
            self.real.login(username, password)
        else:
             if username == "userNotName":
                 return False
             else:
                 return True

    def showProductStore(self, store):
        if self.real != None:
            self.real.showProductStore(store)
        else:
            return True


    def add_product_to_Store(self, StoreID, product_name: str, product_price: int,
                             product_categories: [str],
                             key_words: [str], amount):
        if self.real != None:
            self.real.add_product_to_Store(self, StoreID)
        else:
            return True

    def searchProduct(self, product, category=None, key_words=None):
        if self.real != None:
            self.real.searchProduct(self, product, category, key_words)
        else:
            return {0:[("Banana", 20, "Food", "Fruits", 10)]}

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

    def logout(self,username):
        if self.real != None:
            self.real.logout(self)
        else:
            if username == "guestuser":
                return False
            else:
                return True

    def get_purchase_history(self):
        if self.real!=None:
            return self.real.get_purchase_history()
        else:
            purchase_type = type('Purchase', (object,), {})
            product_type = type('Product', (object,), {})
            p = product_type()
            p.name = "Banana"
            pur = purchase_type()
            pur.products = [p]
            return pur

    def add_product(self,store_id,product,amount):
        if self.real !=None:
            return self.real.add_product(store_id,product,amount)
        else:
            return True

    def buy(self):
        if self.real != None:
            return self.real.buy()
        else:
            return True