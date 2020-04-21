from project.domain_layer.external_managment.PaymentSystem import PaymentSystem
from project.service_layer.StoresManagerInterface import StoresManagerInterface
from project.service_layer.UsersManagerInterface import UsersManagerInterface
from project.domain_layer.external_managment.ShipmentSystemInterface import ShipmentSystemInterface


class PurchaseManager:
    def __init__(self, user_manager: UsersManagerInterface, store_manager: StoresManagerInterface):
        self.user_manager = user_manager
        self.store_manager = store_manager
        self.payment_system = PaymentSystem()
        self.shipment_system = ShipmentSystemInterface()

    def set_external_shipment(self, external_shipment_system):
        self.shipment_system.set_external(external_shipment_system)

    def connect_shipment(self):
        return self.shipment_system.connect()

    def set_external_payment(self, external_payment_system):
        self.shipment_system.set_external(external_payment_system)

    def connect_payment(self):
        return self.payment_system.connect()

    def buy(self, user):
        purchases = self.payment_system.pay(user, self.user_manager.view_cart(user))
        if len(purchases) > 0:
            if self.shipment_system.ship():
                for purchase in purchases:
                    self.store_manager.buy(self.user_manager.view_cart(user))
                    self.store_manager.add_purchase_to_store(purchase.store_id, purchase)
                    self.user_manager.add_purchase(user, purchase)
                self.user_manager.remove_cart(user)
            else:
                self.payment_system.cancel(purchases)
