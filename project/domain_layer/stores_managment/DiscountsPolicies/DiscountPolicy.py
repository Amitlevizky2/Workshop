from abc import ABC, abstractmethod
from datetime import date, datetime

from project.domain_layer.stores_managment import Product


class Discount(ABC):
    _ID = 0

    def __init__(self, start_date, end_date, percent):
        self.id = -1
        self.start = start_date
        self.end = end_date
        self.discount = percent / 100
        self.is_valid = start_date < datetime.today() < end_date
        self.is_commited = False
        self.products_in_discount = {}  # {product_name: bool}
        self.discount_type = ""

    @abstractmethod
    def commit_discount(self, product_price_dict: dict):  # {Product, (amount, updated_price)}
        pass

    # @abstractmethod
    # def is_approved(self, original_price, amount):
    #     pass

    @abstractmethod
    def is_in_discount(self, product_name: str, product_price_dict):
        pass

    @abstractmethod
    def get_discount_type(self):
        pass

    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def get_jsn_description(self):
        pass

    def set_id(self, d_id: int):
        self.id = d_id

    def add_product(self, product_name: str):
        self.products_in_discount[product_name] = True

    def remove_product(self, product_name: str):
        del self.products_in_discount[product_name]

    def get_products(self):
        return self.products_in_discount.keys()

    def is_valid_start_date(self, _date):
        return _date > date.today()

    def is_valid_end_date(self, end_date):
        return end_date > self.start and end_date > date.today()

    def is_valid_percent(self, percent):
        return 0 <= percent <= 100