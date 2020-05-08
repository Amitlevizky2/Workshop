from abc import ABC, abstractmethod


class PurchasePolicy(ABC):
    def __init__(self):
        self.purchase_type = ""

    @abstractmethod
    def is_approved(self, product_price_dict: dict):  # {Product, (amount, updated_price, original_price)}
        pass

    @abstractmethod
    def get_type(self):  # {Product, (amount, updated_price, original_price)}
        pass

