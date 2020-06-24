from abc import ABC, abstractmethod
from datetime import date, datetime

from project.data_access_layer.DiscountORM import DiscountORM
from project.domain_layer.stores_managment import Product


class Discount(ABC):
    _ID = 0

    def __init__(self, start_date, end_date, percent, store_id, orm = None):
        self.id = -1
        self.start = start_date
        self.end = end_date
        self.store_id = store_id
        self.discount = float(percent / 100)
        self.is_valid = start_date < datetime.today() < end_date
        self.is_commited = False
        self.products_in_discount = {}  # {product_name: bool}
        self.discount_type = ""
        self.orm = orm

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

    @abstractmethod
    def get_updated_price(self, product: Product):
        pass

    def set_id(self, d_id: int):
        self.id = d_id
        self.createORM()

    def add_product(self, product_name: str):
        self.products_in_discount[product_name] = True
        self.orm.add_product(product_name)

    def remove_products(self, products=[]):
        for product_name in products:
            self.remove_product(product_name)

    def remove_product(self, product_name: str):
        del self.products_in_discount[product_name]
        self.orm.remove_product(product_name)

    def get_products(self):
        return self.products_in_discount.keys()

    def is_valid_start_date(self, _date):
        return _date > datetime.today()

    def is_valid_end_date(self, end_date):
        return end_date > self.start and end_date > datetime.today()

    def is_valid_percent(self, percent):
        return 0 <= percent <= 100

    def createORM(self):
        if self.orm is None:
            self.orm = DiscountORM()
            self.orm.discount_id= self.id
            self.orm.start_date = self.start
            self.orm.end_date = self.end
            self.orm.percent = self.discount
            self.orm.add()

    def get_set(self, _dict):
        ret = set()
        for element in _dict.keys():
            if _dict[element] is True:
                ret.add(element)
        return ret

    def get_relative_complement(self, new_products_set):
        curr_products_in_discount = self.get_set(self.products_in_discount)
        new_products_in_discount = self.get_set(new_products_set)
