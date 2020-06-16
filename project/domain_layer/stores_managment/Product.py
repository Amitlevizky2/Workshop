from functools import reduce
import datetime


class Product:
    def __init__(self, name, price, categories, key_words, amount):
        self.name = name
        self.original_price = price
        self.categories = categories
        self.key_words = key_words
        self.rate = 0
        self.amount = amount

    def __eq__(self, other):
        return self.name == other.name and \
               self.original_price == other.original_price and \
               self.categories == other.categories and \
               self.original_price == other.original_price and \
               self.key_words == other.key_words and \
               self.rate == other.rate


    def get_price_before_discount(self):
        return self.original_price

    def get_price_by_amount(self, amount):
        return amount * self.original_price

    def reduce_amount(self, to_reduce):
        if to_reduce > self.amount:
            return {'error': True,
                    'error_msg': 'There is not enough quantity in store'}
        self.amount -= to_reduce
        return {'error': False,
                'data': 'Product amount reduced'}
