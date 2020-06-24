import jsonpickle
import jsons
import transaction
from project.domain_layer.external_managment.PaymentSystem import PaymentSystem
from project.domain_layer.external_managment.Purchase import Purchase
from project.domain_layer.users_managment import Cart
from project.service_layer.StoresManagerInterface import StoresManagerInterface
from project.service_layer.UsersManagerInterface import UsersManagerInterface
from project.domain_layer.external_managment.ShipmentSystemInterface import ShipmentSystemInterface


class PurchaseManager:
    def __init__(self, user_manager: UsersManagerInterface, store_manager: StoresManagerInterface):
        self.purchases_idx = 0
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

# user = username
    def buy(self, user,CCnumber,CCmonth,CCyear,CCholder,CCccv,CCid,address,city,country,zip):
        try:
            answer, data = self.user_manager.get_cart(user)
            if answer is False:
                return {'error': not answer,
                        'error_msg': data.error_msg}
            cart = data
            cart_description = jsons.loads(self.store_manager.get_cart_description(cart))

            error = cart_description['ans']
            cart_price = cart_description['cart_price']
            cart_desc = cart_description['cart_description']

            cart_validity = jsons.loads(self.store_manager.check_cart_validity(cart))
            error_validity = cart_validity['error']
            description_validity = cart_validity['description']

            valid_user = self.payment_system.check_user(user, cart_price)  # TRUE/FALSE

            if error:
                if not error_validity:
                    if valid_user:
                        purchases = []
                        for store_basket in cart_desc.values():
                            store_id = store_basket['store_id']
                            self.payment_system.pay(user, store_id, store_basket['store_purchase_price'],CCnumber,CCmonth,CCyear,CCholder,CCccv,CCid)
                            self.purchases_idx += 1
                            purchase = Purchase(store_basket['desc'], user, store_id, self.purchases_idx)
                            print()
                            purchases.append(purchase)
                            self.store_manager.add_purchase_to_store(store_id, purchase)

                        self.store_manager.buy(cart)
                        self.user_manager.add_purchase(user, purchases)
                        self.user_manager.remove_cart(user)

                        return {'error': False,
                                'data': 'Purchase Confirmed!'}

                    else:
                        return {'error': True,
                                'error_msg': 'User does not have enough credit!'}
                else:
                    print('description_validity')
                    print(description_validity)
                    return {'error': True,
                            'error_msg': description_validity}
            else:
                return {'error': True,
                        'error_msg': 'Undefined - get_cart_description'}

            purchases = jsonpickle.decode(self.payment_system.pay(user,store_id,price,CCnumber,CCmonth,CCyear,CCholder,CCccv,CCid))
            if len(purchases) > 0:
                if self.shipment_system.ship(CCholder,address,city,country,zip):
                    for purchase in purchases:
                        self.store_manager.buy(self.user_manager.get_cart(user))
                        self.store_manager.add_purchase_to_store(int(purchase.store_id), jsonpickle.encode(purchase))
                        self.user_manager.add_purchase(user, jsonpickle.encode(purchase))
                    self.user_manager.remove_cart(user)
                    return True
                elif self.payment_system.cancel(purchases) == -1:
                    return False
                transaction.commit()
        except "Transaction Faild":
            transaction.abort()



    def pay(self, user, cart):
        return True

    def connect(self):
        return True
