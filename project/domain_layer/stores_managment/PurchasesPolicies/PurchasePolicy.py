from abc import ABC, abstractmethod


class PurchasePolicy(ABC):
    def __init__(self):
        self.purchase_type = ""
        self.id = -1

    @abstractmethod
    def is_approved(self, product_price_dict: dict):  # {Product, (amount, updated_price, original_price)}
        pass

    @abstractmethod
    def get_type(self):  # {Product, (amount, updated_price, original_price)}
        pass

    @abstractmethod
    def get_description(self):
        pass

    def set_id(self, p_id: int):
        self.id = p_id
