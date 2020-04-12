from functools import reduce
import datetime


class Discount(object):
    def __init__(self, start_date, end_date, percent):
        self.start = start_date
        self.end = end_date
        self.discount = 1 - percent / 100


class Product:
    def __init__(self, name, price, categories, key_words):
        self.name = name
        self.price = price
        self.categories = categories
        self.price = price
        self.key_words = key_words
        self.rate = 0
        self.discount = [Discount]

    def __eq__(self, other):
        return self.name == other.name and \
               self.price == other.price and \
               self.categories == other.categories and \
               self.price == other.price and \
               self.key_words == other.key_words and \
               self.rate == other.rate

    def get_price(self):
        rel_discount = map(
            lambda discount: discount.discount if discount.start < datetime.datetime.now() < discount.end else 1,
            self.discount)
        return self.price * reduce(lambda x, y: x * y, rel_discount)
