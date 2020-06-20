from project.data_access_layer.StorePolicyORM import StorePolicyORM
from project.domain_layer.stores_managment.PurchasesPolicies.PurchasePolicy import PurchasePolicy


class PurchaseStorePolicy(PurchasePolicy):
    def __init__(self, min_amount_products, max_amount_products, id: int, store_id, orm=None):
        super().__init__()
        self.min_amount_products = min_amount_products
        self.max_amount_products = max_amount_products
        self.id = id
        # self.products_int_policy = {}  # {product_name, bool}
        self.MAX_SIZE = 100000
        self.MIN_SIZE = 0
        self.store_id =store_id
        self.purchase_type = "Purchase Store Policy"
        if orm is None:
            self.orm = StorePolicyORM()
            self.orm.policy_id = id
            self.orm.store_id = store_id
            self.orm.min_amount = min_amount_products
            self.orm.max_amount = max_amount_products
            self.orm.add()

    def is_approved(self, product_price_dict: dict):    #    {"product name",(Product, amount)}
        outcome_description = ""
        basket_size = self.total_num_products([*product_price_dict.values()])
        is_approved = self.min_amount_products <= basket_size <= self.max_amount_products
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
        desc = "You have [{}] products in your basket and you can only buy minimum [{}] and maximum [{}] products in this store\n".\
            format(str_basket_size, min_string, max_string)
        return desc

    def get_type(self):
        return self.purchase_type

    def total_num_products(self, product_amount_tup: list):
        total_amount = 0
        for product in product_amount_tup:
            total_amount += product[1]
        return total_amount

    def get_description(self):
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

        return [self.id, self.purchase_type, min_string, max_string]