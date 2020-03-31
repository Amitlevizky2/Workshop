from project.domain_layer.stores_managment.Product import Product


class Inventory:
    def __init__(self):
        # products = {"product name",(Product,amount,price,?discount?)}
        self.products = {}

    def add_product(self, product_name, product: Product, amount=0, price=0):
        """

        Args:
            product_name:
            product:
            amount:
            price:
        """
        self.products[product_name] = (product, amount, price)
