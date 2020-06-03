from project.data_access_layer.ProductORM import ProductORM


class Product:
    def __init__(self, name, price, categories, key_words, amount,store_id):
        self.name = name
        self.original_price = price
        self.categories = categories
        self.key_words = key_words
        self.rate = 0
        self.amount = amount
        self.visible_discount = []
        self.conditional_product_discount = []
        self.orm =  ProductORM()
        self.orm.name = name
        self.orm.store_id = store_id

    def __eq__(self, other):
        return self.name == other.name and \
               self.original_price == other.price and \
               self.categories == other.categories and \
               self.original_price == other.price and \
               self.key_words == other.key_words and \
               self.rate == other.rate

    def get_price_after_discount(self, amount_to_buy):
        return self.price_after_discounts
        # price_after_discount = self.original_price
        # for discount in self.visible_discount:
        #     price_after_discount = discount.commit_discount(price_after_discount, amount_to_buy)
        #
        # price_after_visible_discount = price_after_discount * amount_to_buy
        # price_after_conditional_product_discount = price_after_visible_discount
        #
        # for discount in self.conditional_product_discount:
        #     price_after_conditional_product_discount -= discount.commit_discount(price_after_discount, amount_to_buy)
        #
        # return price_after_conditional_product_discount

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

    def edit_conditional_product_discount(self, discount_id, start_date, end_date, percent, conditions):
        cur_disc = None
        for disc in self.conditional_product_discount:
            if disc.id == discount_id:
                cur_disc = disc

        if cur_disc:
            cur_disc.edit_product_discount(start_date, end_date, percent, conditions)
            return True
        return False

    def get_price_by_amount(self, amount):
        return amount * self.original_price

    def reduce_amount(self, to_reduce):
        if to_reduce > self.amount:
            return False
        self.amount -= to_reduce
        x=5