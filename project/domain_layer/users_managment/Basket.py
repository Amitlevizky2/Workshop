from project.data_access_layer.BasketORM import BasketORM


class Basket:

    # send the initial product to init????
    def __init__(self, username, store_id, orm=None):
        # products = {"product name",amount}
        self.products = {}
        self.store_id = store_id
        self.username = username
        if not username.startswith('guest'):
            if orm is None:
                self.orm = BasketORM()
                self.orm.username = username
                self.orm.store_id = store_id
                self.orm.add()
            else:
                self.orm = orm

    # check += ???????
    def add_product(self, product_name, quantity) -> bool:
        if product_name in self.products.keys():
            amount = self.products[product_name]
            amount += quantity
            self.products[product_name] = amount
            if not self.username.startswith('guest'):
                self.orm.update_basket_product_quantity(product_name, amount)
        else:
            self.products[product_name] = quantity
            if not self.username.startswith('guest'):
                self.orm.update_basket_add_product(product_name, quantity)
        return True

    def remove_product(self, product_name, quantity) -> bool:
        if product_name in self.products.keys():
            amount = self.products[product_name]
            amount = amount - quantity
            if amount <= 0:
                self.products.pop(product_name)
                self.orm.remove_product_from_basket(product_name)
                if self.products.keys().__len__() == 0:
                    self.products = {}
                    if not self.username.startswith('guest'):
                        self.orm.remove_basket()
            else:
                self.products[product_name] = amount
                if not self.username.startswith('guest'):
                    self.orm.update_basket_product_quantity(product_name, quantity)
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
