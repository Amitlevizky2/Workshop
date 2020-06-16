from functools import reduce
import datetime




class Discount(object):
    def __init__(self, start_date, end_date, percent):
        self.start = start_date
        self.end = end_date
        self.discount = 1 - percent / 100


class Product:
    def __init__(self, name, price, categories, key_words, amount, store_id, orm = None):
        from project.data_access_layer.ProductORM import ProductORM
        self.name = name
        self.original_price = price
        self.categories = categories
        self.key_words = key_words
        self.rate = 0
        self.amount = amount
        if orm is None:
            self.orm = ProductORM()
            self.orm.name = name
            self.orm.store_id = store_id
            self.orm.categories = ','.join(categories)
            self.orm.key_words =','. join(key_words)
            self.orm.price = price
            self.orm.quantity = amount
            self.orm.add()
        else:
            self.orm = orm

    # def __init__(self, name, price, categories, key_words, amount, store_id, orm):
    #     self.name = name
    #     self.original_price = price
    #     self.categories = categories
    #     self.key_words = key_words
    #     self.rate = 0
    #     self.amount = amount
    #     self.orm = orm



    def __eq__(self, other):
        return self.name == other.name and \
               self.original_price == other.original_price and \
               self.categories == other.categories and \
               self.original_price == other.original_price and \
               self.key_words == other.key_words and \
               self.rate == other.rate


    def get_price_before_discount(self):
        return self.original_price

    def add_visible_discount(self, discount):
        self.visible_discount.append(discount)

    def add_conditional_product_discount(self, discount):
        self.conditional_product_discount.append(discount)

    # def add_conditional_store_discount(self, discount):
    #     self.conditional_store_discount.append(discount)

    def edit_visible_discount(self, discount_id, start_date, end_date, percent):
        cur_disc = None
        for disc in self.visible_discount:
            if disc.id == discount_id:
                cur_disc = disc

        if cur_disc:
            cur_disc.edit_visible_discount(start_date, end_date, percent)
            return True
        return False

    def get_price_by_amount(self, amount):
        return amount * self.original_price

    def reduce_amount(self, to_reduce):
        if to_reduce > self.amount:
            return False
        self.amount -= to_reduce
        self.orm.update_product_amount(self.name, self.orm.store_id, self.amount)
        x = 5

    def get_jsn_description(self):
        return {"Name": self.name,
                "Original Price": self.original_price,
                "Categories": self.categories,
                "Keywords": self.key_words,
                "Rate": self.rate,
                "Amount": self.amount}
