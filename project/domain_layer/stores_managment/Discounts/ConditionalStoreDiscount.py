from project.domain_layer.stores_managment.Discounts.DiscountPolicy import Discount



class ConditionalStoreDiscount(Discount):
    def __init__(self, start_date, end_date, percent, discount_conditions):
        super().__init__(start_date, end_date, percent)
        self.discount_conditions = discount_conditions

    def commit_discount(self, product_price_dict: dict):
        pass

    def edit_discount(self, start_date=None, end_date=None, percent=None, discount_conditions=None):
        if start_date is not None and end_date is not None:
            if start_date > end_date:
                return False
        if start_date is not None and is_valid_start_date(start_date):
            self.start = start_date
        if end_date is not None and is_valid_end_date(end_date):
            self.end = end_date
        if percent is not None and is_valid_percent(percent):
            self.discount = 1 - percent / 100
        if discount_conditions is not None:
            self.discount_conditions.append(discount_conditions)

    def is_approved(self, original_price, amount):
        pass

    def undu_discount(self, original_price, amount):
        pass

