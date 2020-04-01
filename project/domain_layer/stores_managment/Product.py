class Product:
    def __init__(self, name, price, category, key_words):
        self.name = name
        self.price = price
        self.category = category
        self.price = price
        self.key_words = key_words
        self.rate = 0


    def __eq__(self, other):
        return self.name == other.name and \
               self.price == other.price and \
               self.category == other.category and \
               self.price == other.price and \
               self.key_words == other.key_words and \
               self.rate == other.rate
