from project.domain_layer.external_managment.Purchase import Purchase
from project.domain_layer.users_managment.Cart import Cart


class PaymentSystem:
    def __init__(self, external_payment_system):
        self.external_payment_system = external_payment_system
        self.p_id = 0

    def pay(self, user, cart: Cart) -> [Purchase]:
        if self.external_payment_system.pay(user, cart):
            res = []
            for store in cart.baskets.keys():
                res.append(Purchase(cart.baskets.get(store).products, user, store, self.p_id))
                self.p_id += 1
            return res
