from project.domain_layer.stores_managment.DiscountsPolicies.DiscountPolicy import Discount
from datetime import date, datetime

from project.domain_layer.users_managment import Basket


class ConditionalProductDiscount(Discount):
    def __init__(self, start_date, end_date, percent, min_amount, num_prods_to_apply):
        super().__init__(start_date, end_date, percent)
        self.min_amount = min_amount
        self.num_prods_to_apply = num_prods_to_apply
        # self.products_in_discount = {}  # {product: bool}
        self.discount_type = "Conditional Product Discount"

    def commit_discount(self, product_price_dict: dict):
        if self.start < datetime.today() < self.end:
            for product_name in product_price_dict.keys():
                product_tup = product_price_dict[product_name]  #  {product_name, (Product, amount, updated_price, original_price)}

                if product_name in self.products_in_discount.keys():
                    new_product_tup = (self.get_product_object(product_tup), self.get_product_amount(product_tup),
                                       self.get_product_updated_price(product_tup), self.get_product_object(product_tup).original_price * self.get_product_amount(product_tup))
                    product_price_dict[
                        product_name] = new_product_tup  # (self.discount * self.get_product_object(product_tup).original_price * self.get_product_amount(product_tup))
                    x = 5

    def get_product_object(self, product):
        return product[0]

    def get_product_amount(self, product):
        return product[1]

    def get_product_updated_price(self, product):
        new_price = product[2] - self.calculate_conditional_discount(product)
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

        for i in range(1, amount_to_buy + 1):
            if min_counter > 0:
                min_counter -= 1

            elif to_apply > 0:
                to_apply -= 1
                counter += 1

            else:
                min_counter = self.min_amount
                to_apply = self.num_prods_to_apply

        return counter

    def edit_discount(self, start_date, end_date, percent, min_amount, num_prods_to_apply):
        is_edited = False
        if start_date is not None and end_date is not None:
            if start_date > end_date:
                return False
        if start_date is not None and start_date > datetime.today():
            self.start = start_date
            is_edited = True
        if end_date is not None and end_date > self.start and end_date > datetime.today():
            self.end = end_date
            is_edited = True
        if percent is not None and 0 < percent < 100:
            self.discount = percent / 100
            is_edited = True
        if min_amount is not None and 0 < min_amount:
            self.min_amount = min_amount
            is_edited = True
        if num_prods_to_apply is not None and 0 < num_prods_to_apply:
            self.num_prods_to_apply = num_prods_to_apply
            is_edited = True

    def is_valid_condition(self, discount_conditions):
        return discount_conditions[0] > 0 and 0 <= discount_conditions <= 100

    def is_approved(self, original_price, amount):
        pass

    def is_product_in_conditions(self, product_tup):
        if self.get_product_object(product_tup).name in self.products_in_discount.keys():
            if self.get_product_amount(product_tup) > self.min_amount:
                return True
        return False

    def is_in_discount(self, product_name: str, product_price_dict: dict):
        if product_name in product_price_dict.keys():
            is_valid = self.is_product_in_conditions(product_price_dict[product_name])
            return product_name in self.products_in_discount and \
                   is_valid
        else:
            return False


    def get_discount_type(self):
        return self.discount_type

