from project.domain_layer.stores_managment.PurchasesPolicies.PurchasePolicy import PurchasePolicy


class PurchaseStorePolicy(PurchasePolicy):
    def __init__(self, min_amount_products, max_amount_products, id: int):
        super().__init__()
        self.min_amount_products = min_amount_products
        self.max_amount_products = max_amount_products
        self.id = id
        self.products_int_policy = {}  # {product_name, bool}
        self.MAX_SIZE = 100000
        self.MIN_SIZE = 0

    def is_approved(self, product_price_dict: dict):
        outcome_description = ""
        basket_size = len(product_price_dict.keys())
        is_approved = self.min_amount_products <= len(product_price_dict.keys()) <= self.max_amount_products
        if not is_approved:
            outcome_description = self.add_fail_description(str(basket_size))
        return is_approved, outcome_description

    def add_fail_description(self, str_basket_size):
        min_string = ""
        max_string = ""
        if self.min_amount_products == self.MIN_SIZE:
            min_string = "no min limit"
        else:
            min_string = str(self.min_amount_products)

        if self.min_amount_products == self.MAX_SIZE:
            max_string = "no max limit"
        else:
            max_string = str(self.max_amount_products)
        desc = "You have {} products in your basket and you can only buy minimum {} and maximum {} products in this store\n".format\
            (str_basket_size, min_string, max_string)
        return desc

