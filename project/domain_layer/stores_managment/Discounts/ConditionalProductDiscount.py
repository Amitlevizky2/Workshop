from project.domain_layer.stores_managment.Discounts.DiscountPolicy import Discount
from datetime import date, datetime

from project.domain_layer.users_managment import Basket


class ConditionalProductDiscount(Discount):
    def __init__(self, start_date, end_date, percent, min_amount, num_prods_to_apply):
        super().__init__(start_date, end_date, percent)
        self.min_amount = min_amount
        self.num_prods_to_apply = num_prods_to_apply
        self.products_in_discount = {}  # {product: bool}

    def commit_discount(self, product_price_dict: dict):
        if self.start < datetime.today() < self.end:
            for product_name in product_price_dict.keys():
                product_tup = product_price_dict[product_name]  #  {product_name, (Product, amount, updated_price)}

                if product_name in self.products_in_discount.keys():
                    new_product_tup = (self.get_product_object(product_tup), self.get_product_amount(product_tup),
                                       self.get_product_updated_price(product_tup))
                    product_price_dict[
                        product_name] = new_product_tup  # (self.discount * self.get_product_object(product_tup).original_price * self.get_product_amount(product_tup))
                    x = 5

    def get_product_object(self, product):
        return product[0]

    def get_product_amount(self, product):
        return product[1]

    def get_product_updated_price(self, product):
        new_price = product[2] - self.get_amount_to_commit(self.get_product_amount(product))
        return new_price

    def calculate_conditional_discount(self, product_tup):
        amount_to_buy = self.get_product_amount(product_tup)
        amount_to_commit_discount = self.get_amount_to_commit(amount_to_buy)
        original_product_price = self.get_product_object(product_tup).original_price
        one_product_discount = original_product_price * self.discount
        return one_product_discount * amount_to_commit_discount

    def get_amount_to_commit(self, amount_to_buy: int):
        counter = 0
        min_counter = self.min_amount
        to_apply = self.num_prods_to_apply

        for i in range(1, amount_to_buy):
            if min_counter > 0:
                min_counter -= 1

            elif to_apply > 0:
                to_apply -= 1
                counter += 1

            else:
                min_counter = self.min_amount
                to_apply = self.num_prods_to_apply

        return counter

    def edit_discount(self, start_date=None, end_date=None, percent=None, min_amount=None, num_prods_to_apply=None):
        if start_date is not None and end_date is not None:
            if start_date > end_date:
                return False
        if start_date is not None and is_valid_start_date(start_date):
            self.start = start_date
        if end_date is not None and is_valid_end_date(end_date):
            self.end = end_date
        if percent is not None and is_valid_percent(percent):
            self.discount = 1 - percent / 100
        if discount_condition is not None and self.is_valid_condition(discount_condition):
            self.discount_condition = discount_condition

    def is_valid_condition(self, discount_conditions):
        return discount_conditions[0] > 0 and 0 <= discount_conditions <= 100

    def is_approved(self, original_price, amount):
        pass

    def undu_discount(self):
        for product in self.products_in_discount.keys():
            if not self.products_in_discount[product]:
                product_quant = product.amount
                num_prods_to_red = int(product_quant / self.min_amount)
                product.price_after_discounts += num_prods_to_red * (
                        self.discount * product.original_price)