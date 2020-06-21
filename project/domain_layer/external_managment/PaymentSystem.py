import jsonpickle

from project import logger
from project.domain_layer.external_managment.Purchase import Purchase
from project.domain_layer.users_managment.Cart import Cart
from project.service_layer.ExternalserviseAPI import ExternalServiceAPI

class PaymentSystem:
    def __init__(self):
        self.external_payment_system = None
        self.p_id = 0
        self.padid = 0
        self.supid=0
        self.EX = ExternalServiceAPI()

    def set_external(self, external_payment_system):
        self.external_payment_system = external_payment_system

    def connect(self):
        if self.external_payment_system is not None:
            x = str(self.EX.connect())
            if x == "OK":
                return True
            logger.error("Failed to connect to payment system")
        return False

    def pay(self, user, store_id, price,CCnumber,CCmonth,CCyear,CCholder,CCccv,CCid):
        try:
            if PaymentSystem.connect(self):
                self.padid = int(self.EX.pay(CCnumber,CCmonth,CCyear,CCholder,CCccv,CCid))
                return self.padid
        except:
            return -1
        # res = []
        # cart = jsonpickle.decode(cart)
        # if True:  # self.external_payment_system.pay(user, cart):
        #     for store in cart.baskets.keys():
        #         res.append(Purchase(cart.baskets.get(store).products, user, store, self.p_id))
        #         self.p_id += 1
        # else:
        #     logger.error("Failed to complete payment")
        # return jsonpickle.encode(res)

    def cancel(self, purchases):
        try:
            int(self.EX.cancelpay(self.padid))
            return 1
        except:
            return -1
            # self.external_payment_system.cancel(purchases)

    def check_user(self, user, cart_price):
        return True
