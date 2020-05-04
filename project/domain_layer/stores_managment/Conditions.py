class ProductCondition():
    def __init__(self, amount_to_apply, percent):
        self.amount_to_apply = amount_to_apply
        self.percent = 1 - percent/100


class StoreCondtion:
    def __init__(self, price_to_apply, percent):
        self.price_to_apply = price_to_apply
        self.percent = 1 - percent / 100
