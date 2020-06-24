import jsonpickle
import jsons
import transaction

from project.domain_layer.external_managment.PaymentSystem import PaymentSystem
from project.domain_layer.external_managment.Purchase import Purchase
from project.domain_layer.users_managment import Cart
from project.service_layer.ExternalserviseAPI import ExternalServiceAPI
from project.service_layer.StoresManagerInterface import StoresManagerInterface
from project.service_layer.UsersManagerInterface import UsersManagerInterface
from project.domain_layer.external_managment.ShipmentSystemInterface import ShipmentSystemInterface


class PurchaseManager:
    def __init__(self, user_manager: UsersManagerInterface, store_manager: StoresManagerInterface):
        self.purchases_idx = 0
        self.user_manager = user_manager
        self.store_manager = store_manager
        self.external_service = ExternalServiceAPI()
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
    def buy(self, user, cc_number, cc_month, cc_year, cc_holder, cc_ccv, cc_id, address, city, country, zip):
        # try:
            answer, data = self.user_manager.get_cart(user)
            if answer is False:
                return {'error': not answer,
                        'error_msg': data['error_msg']}
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
                        purchases = {}
                        for store_basket in cart_desc.values():
                            store_id = store_basket['store_id']
                            # self.payment_system.pay(cc_number, cc_month, cc_year, cc_holder, cc_ccv, cc_id)
                            self.purchases_idx += 1
                            purchase = Purchase(store_basket['desc'], user, store_id, self.purchases_idx)
                            print(jsons.dumps(purchase))
                            purchases[store_id] = purchase
                            # self.store_manager.add_purchase_to_store(store_id, purchase)
                        print('BEFORE PAYYYYYYYYYYY')
                        payment_reciept = self.external_service.pay(cc_number, cc_month, cc_year, cc_holder, cc_ccv,
                                                                    cc_id)
                        print('payment_reciept')
                        print(payment_reciept)
                        if payment_reciept > 0:
                            if len(purchases.keys()) > 0:
                                supply_reciept = self.external_service.supply(cc_holder, address, city, country, zip)
                                print('supply_reciept')
                                print(supply_reciept)
                                if supply_reciept > 0:
                                    self.store_manager.buy(cart)
                                    self.update_purchase_number(purchases, payment_reciept, supply_reciept)
                                    self.user_manager.add_purchase(user, purchases)
                                    self.add_purchases_to_stores(purchases)
                                    self.user_manager.remove_cart(user)

                                    return {'error': False,
                                            'data': 'Purchase Confirmed!'}
                                else:
                                    # self.external_service.cancelpay(payment_reciept)
                                    return {'error': True,
                                            'data': 'Purchase Canceled'}
                            else:
                                self.external_service.cancelpay(payment_reciept)
                                return {'error': True,
                                        'data': 'Purchase Canceled'}
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
            transaction.commit()
        # except:
        #     print('AFTER PAYYYYYYYYYYY')
        #     transaction.abort()

    def connect(self):
        return True

    def cancel_pay(self, receipt: int):
        cancel = self.external_service.cancelpay(receipt)
        if cancel == 1:
            return {
                'error': False,
                'error_msg': 'Money returned'
            }
        else:
            return {
                'error': True,
                'error_msg': 'Invalid receipt'
            }

    def cancel_supply(self, receipt: int):
        cancel = self.external_service.cancelsupply(receipt)
        if cancel == 1:
            return {
                'error': False,
                'error_msg': 'supply returned'
            }
        else:
            return {
                'error': True,
                'error_msg': 'Invalid receipt'
            }

    def add_purchases_to_stores(self, purchases):
        for store_id in purchases.keys():
            self.store_manager.stores_manager.add_purchase_to_store(store_id, purchases[store_id])

    def update_purchase_number(self, purchases, order_number: int, supply_number: int):
        for purchase in purchases.values():
            purchase.set_order_number(order_number)
            purchase.set_supply_number(supply_number)
