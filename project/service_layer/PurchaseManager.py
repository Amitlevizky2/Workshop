from project.domain_layer.external_managment.PaymentSystem import PaymentSystem
from project.domain_layer.external_managment.ShipmentSystem import ShipmentSystem
from project.service_layer.StoresManagerInterface import StoresManagerInterface
from project.service_layer.UsersManagerInterface import UsersManagerInterface


class PurchaseManager:
    def __init__(self, user_manager:UsersManagerInterface , store_manager: StoresManagerInterface):
        self.user_manager = user_manager
        self.store_manager = store_manager
        self.payment_system = PaymentSystem()
        self.shipment_system = ShipmentSystem()

    def buy(self, user):
        for purchase in self.payment_system.pay(user, self.user_manager.view_cart(user)):
            self.user_manager.add_purchase(user, purchase)
            self.store_manager.add_purchase_to_store(purchase.store_id, purchase)
        self.shipment_system.ship()
        self.user_manager.remove_cart(user)
