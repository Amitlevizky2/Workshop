from project.domain_layer.stores_managment.Product import Product


class Inventory:
    def __init__(self):
        # products = {"product name", Product}
        self.products = {}

    def add_product(self, product_name, product: Product, amount=0, price=0):
        """

        Args:
            product_name:
            product:
            amount:
            price:
        """
        self.products[product_name] = product

    # def remove_product(self, product_name):
    #     self.products.pop(product_name)

    def update_product(self, product_name, attribute, updated):
        if product_name in self.products.keys():
            if attribute == "discount":
                self.products.get(product_name).visible_discount.append(updated)
            else:
                setattr(self.products.get(product_name), attribute, updated)
            return True
        return False

    def buy_product(self, product_name, amount):
        if product_name not in self.products.keys():
            return {'error': True,
                    'error_msg': 'No such product: ' + product_name}
        if amount < 0:
            return {'error': True,
                    'error_msg': 'amount < 0'}
        return self.products[product_name].reduce_amount(amount)

    def get_products(self):
        return self.products

    def remove_product(self, product_name):
        if product_name in self.products.keys():
            self.products.pop(product_name)
            return True
        return False

    def get_description(self):
        products = {}
        for product in self.products.values():
            products[product.name] = [product.amount, product.original_price]
        return products

    def get_jsn_description(self):
        products_dict_list = []
        for tup in self.products.values():
            products_dict_list.append(tup.get_jsn_description())
        return products_dict_list

    def get_product(self, product_name):
        product = self.products[product_name]
        return product

    def is_valid_amount(self, product_name, quantity):
        product = self.get_product(product_name)
        valid_amount = -1
        if product is not None:
            valid_amount = product.amount - quantity
        return {
            'error': not (valid_amount >= 0),
            'error_msg': 'Sorry, we have only {} pieces of the product {}.'.format(str(product.amount), product_name),
            'data': 'valid amount'
        }
