class Product:
    def __init__(self, name, price, categories, key_words, amount):
        self.name = name
        self.price = price
        self.categories = categories
        self.key_words = key_words
        self.rate = 0
        self.amount = amount
        self.visible_discount = []
        self.conditional_product_discount = []

    def __eq__(self, other):
        return self.name == other.name and \
               self.price == other.price and \
               self.categories == other.categories and \
               self.price == other.price and \
               self.key_words == other.key_words and \
               self.rate == other.rate

    def get_price_after_discount(self, amount_to_buy):
        price_after_discount = self.price
        for discount in self.visible_discount:
            price_after_discount = discount.commit_discount(price_after_discount, amount_to_buy)

        price_after_visible_discount = price_after_discount * amount_to_buy
        price_after_conditional_product_discount = price_after_visible_discount

        for discount in self.conditional_product_discount:
            price_after_conditional_product_discount -= discount.commit_discount(price_after_discount, amount_to_buy)

        return price_after_conditional_product_discount

    def get_price_before_discount(self):
        return self.price

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
