from abc import ABC, abstractmethod


class PurchasePolicy(ABC):
    def __init__(self, p_id, store_id, orm = None):
        self.purchase_type = ""
        self.id = p_id
        self.store_id = store_id
        # if orm is None:
        #     from project.data_access_layer.PolicyORM import PolicyORM
        #     self.orm = PolicyORM()
        #     self.orm.p_id = p_id
        #     self.orm.store_id = self.store_id
        #     self.orm.add()
        # else:
        self.orm = orm

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
        self.createORM()

    def createORM(self):
        if self.orm is None:
            from project.data_access_layer.PolicyORM import PolicyORM
            self.orm = PolicyORM()
            self.orm.policy_id = self.id
            self.orm.store_id = self.store_id

