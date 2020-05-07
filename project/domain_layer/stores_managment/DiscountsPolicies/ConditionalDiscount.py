import datetime

from project.domain_layer.stores_managment.DiscountsPolicies.DiscountPolicy import Discount


class ConditionalDiscount(Discount):
    def __init__(self, start_date, end_date, percent, min_amount, num_prods_to_apply):
        super().__init__(start_date, end_date, percent)
        pass

    def commit_discount(self, product_price_dict: dict):
        pass

    def is_approved(self, original_price, amount):
        pass



    def edit_discount(self):
        pass