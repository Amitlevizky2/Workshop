from project.domain_layer.external_managment.PaymentSystem import PaymentSystem
from project.service_layer.StoresManagerInterface import StoresManagerInterface
from project.service_layer.UsersManagerInterface import UsersManagerInterface


class PurchaseManager:
    def __init__(self, user_manager:UsersManagerInterface , store_manager: StoresManagerInterface):
        self.user_manager = user_manager
        self.store_manager = store_manager
        self.payment_system = PaymentSystem()

    def buy(self, user):
        for purchase in self.payment_system.pay(user, self.user_manager.get_cart(user)):
            self.user_manager.add_purchase(user, purchase)
            self.store_manager.add_purchase_to_store(purchase.store_id, purchase)
