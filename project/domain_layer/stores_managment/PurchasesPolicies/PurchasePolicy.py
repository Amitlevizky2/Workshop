from abc import ABC, abstractmethod


class PurchasePolicy(ABC):
    @abstractmethod
    def is_approved(self, product_price_dict: dict):  # {Product, (amount, updated_price, original_price)}
        pass

