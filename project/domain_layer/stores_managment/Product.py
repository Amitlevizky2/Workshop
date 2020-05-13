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

    def get_price_after_discount(self):
        price_after_discount = self.price
        for discount in self.discount:
            price_after_discount = price_after_discount * discount.discount
        return price_after_discount

    def get_price_before_discount(self):
        return self.price

    def add_discount(self, discount):
        self.discount.append(discount)
