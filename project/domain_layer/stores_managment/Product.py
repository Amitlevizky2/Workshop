from functools import reduce
import datetime


class Discount(object):
    def __init__(self, start_date, end_date, percent):
        self.start = start_date
        self.end = end_date
        self.discount = 1 - percent / 100


class Product:
    def __init__(self, name, price, categories, key_words, amount):
        self.name = name
        self.price = price
        self.categories = categories
        self.key_words = key_words
        self.rate = 0
        self.amount = amount
        self.discount = []

    def __eq__(self, other):
        return self.name == other.name and \
               self.price == other.price and \
               self.categories == other.categories and \
               self.price == other.price and \
               self.key_words == other.key_words and \
               self.rate == other.rate

    def get_price(self):
        for discount in self.discount:
            self.price = self.price * discount.discount
        return self.price
