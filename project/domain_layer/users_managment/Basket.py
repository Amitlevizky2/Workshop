class Basket:
    # send the initial product to init????
    def __init__(self, store_id):
        # products = {"product name",amount}
        self.products = {}
        self.store_id = store_id
        self.total = 0

    def get_total(self):
        total = 0
        for product in self.products.values():
            total += product[0].get_price_after_discount(product[1])
        self.total = total

        return self.total

    # check += ???????
    def add_product(self, product_name, quantity) -> bool:
        if product_name in self.products.keys():
            amount = self.products[product_name]
            amount += quantity
            self.products[product_name] = amount
        else:
            self.products[product_name] = quantity
        return True

    def remove_product(self, product_name, quantity) -> bool:
        if product_name in self.products.keys():
            amount = self.products[product_name]
            amount = amount - quantity
            if amount <= 0:
                self.products.pop(product_name)
                if self.products.keys().__len__() == 0:
                    self.products = {}
            else:
                self.products[product_name] = amount
            return True
        return False

    def get_jsn_description(self):
        """
        :return:
        basket =
        {
            store_id: self.store_id
            products:
            [
                {
                    product_name: product1,
                    amount: x1
                },
                {
                    product_name: product2,
                    amount: x2
                }
                ...
                {
                    product_name: productN,
                    amount: xN
                }
            ]
        }
        """
        products_description = []
        for key, value in self.products.items():
            products_description.append({
                'product_name': key,
                'amount': value[1]
            })
        return {
            'store_id': self.store_id,
            'products': products_description
        }
