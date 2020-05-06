from abc import ABC, abstractmethod
from datetime import date, datetime

from project.domain_layer.stores_managment import Product


class Discount(ABC):
    _ID = 0

    def __init__(self, start_date, end_date, percent):
        self.id = self._ID
        self.__class__._ID += 1
        self.start = start_date
        self.end = end_date
        self.discount = percent / 100
        self.is_valid = start_date < datetime.today() < end_date
        self.is_commited = False

    @abstractmethod
    def commit_discount(self, product_price_dict: dict):  # {Product, (amount, updated_price)}
        pass

    @abstractmethod
    def is_approved(self, original_price, amount):
        pass

    @abstractmethod
    def undu_discount(self):
        pass

    @abstractmethod
    def edit_discount(self):
        pass

    def is_valid_start_date(self, _date):
        return _date > date.today()

    def is_valid_end_date(self, end_date):
        return end_date > self.start and end_date > date.today()

    def is_valid_percent(self, percent):
        return 0 < percent < 100