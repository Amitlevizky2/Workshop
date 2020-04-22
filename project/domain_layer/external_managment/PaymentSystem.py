import jsonpickle

from project import logger
from project.domain_layer.external_managment.Purchase import Purchase
from project.domain_layer.users_managment.Cart import Cart


class PaymentSystem:
    def __init__(self):
        self.external_payment_system = None
        self.p_id = 0

    def set_external(self, external_payment_system):
        self.external_payment_system = external_payment_system

    def connect(self):
        if self.external_payment_system is not None:
            if self.external_payment_system.connect():
                return True
            logger.error("Failed to connect to payment system")
        return False

    def pay(self, user, cart: Cart) -> [Purchase]:
        res = []
        cart = jsonpickle.decode(cart)
        if self.external_payment_system.pay(user, cart):

            for store in cart.baskets.keys():
                res.append(Purchase(cart.baskets.get(store).products, user, store, self.p_id))
                self.p_id += 1
        else:
            logger.error("Failed to complete payment")
        return jsonpickle.encode(res)

    def cancel(self, purchases):
        self.external_payment_system.cancel(purchases)
