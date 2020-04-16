class Basket:
    # send the initial product to init????
    def __init__(self, store_id):
        # products = {"product name",(Product, amount)}
        self.products = {}
        self.store_id = store_id
        self.total = 0

    def get_total(self):
        total = 0
        for product in self.products.values():
            total += product[0].get_price() * (product[1])
        self.total = total
        return self.total

    # check += ???????
    def add_product(self, product, quantity):
        if product.name in self.products.keys():
            amount = self.products[product.name][1]
            amount += quantity
            self.products[product.name] = (product, amount)
        else:
            self.products[product.name] = (product, quantity)
        return True

    def remove_product(self, product, quantity):
        if product.name in self.products.keys():
            amount = self.products[product.name][1]
            amount = amount - quantity
            if amount <= 0:
                self.products.pop(product.name)
                if self.products.keys().__len__() == 0:
                    self.products = {}
            else:
                self.products[product.name] = (product, amount)
