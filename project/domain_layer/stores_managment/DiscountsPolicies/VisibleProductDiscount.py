from project.domain_layer.stores_managment import Product
from project.domain_layer.stores_managment.DiscountsPolicies.DiscountPolicy import Discount
from datetime import date, datetime


class VisibleProductDiscount(Discount):
    def __init__(self, start_date, end_date, percent):
        super().__init__(start_date, end_date, percent)
        self.discount_type = "Visible Discount"
        # self.products_in_discount = {}  # {product_name: bool}

    def commit_discount(self, product_price_dict: dict):  # {product_name, (Product, amount, updated_price, original)}

        if self.start < datetime.today() < self.end:
            for product_name in product_price_dict.keys():
                product_tup = product_price_dict[product_name]

                if product_name in self.products_in_discount.keys():
                    new_product_tup = (self.get_product_object(product_tup), self.get_product_amount(product_tup),
                                       self.get_product_updated_price(product_tup, self.discount), self.get_product_object(product_tup).original_price * self.get_product_amount(product_tup))
                    product_price_dict[product_name] = new_product_tup  # (self.discount * self.get_product_object(product_tup).original_price * self.get_product_amount(product_tup))
                    x=5

    def get_product_object(self, product):
        return product[0]

    def get_product_amount(self, product):
        return product[1]

    def get_product_updated_price(self, product, discount):
        new_price = product[2] - (self.discount * self.get_product_object(product).original_price * self.get_product_amount(product))
        return new_price

    def is_valid_start_date(self, _date):
        super().is_valid_start_date(_date)

    def is_valid_end_date(self, end_date):
        super().is_valid_end_date(end_date)

    def is_valid_percent(self, percent):
        super().is_valid_percent(percent)

    def is_approved(self, original_price, amount):
        pass

    def edit_discount(self, start_date=None, end_date=None, percent=None):
        if start_date is not None and end_date is not None:
            if start_date > end_date:
                return False
        if start_date is not None and is_valid_start_date(start_date):
            self.start = start_date
        if end_date is not None and is_valid_end_date(end_date):
            self.end = end_date
        if percent is not None and is_valid_percent(percent):
            self.discount = 1 - percent / 100

    def is_in_discount(self, product_name: str, product_price_dict: dict):
        return product_name in self.products_in_discount and \
               product_name in product_price_dict.keys()

    def get_discount_type(self):
        return self.discount_type

    def get_description(self):
        return [self.id, self.discount_type, self.start, self.end, self.discount, self.products_in_discount]

    def get_updated_price(self, product: Product):
        if product.name in self.products_in_discount.keys():
            return (product.original_price - product.original_price * self.discount)
        else:
            return product.original_price

    def get_jsn_description(self):
        return {"Start Date": self.start.strftime('%m/%d/%Y'),
                "End Date": self.end.strftime('%m/%d/%Y'),
                "Percent": self.discount,
                "Products In Discount": self.products_in_discount.keys(),
                "Discount Type": self.discount_type}
