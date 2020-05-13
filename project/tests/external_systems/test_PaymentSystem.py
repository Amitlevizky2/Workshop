import unittest

import jsonpickle

from project.domain_layer.external_managment.PaymentSystem import PaymentSystem
from project.domain_layer.users_managment.Cart import Cart


class external_paymentstub:
    def connect(self):
        return True

    def pay(self,user,purchase_data):
        return True


class failed_paymenstub:
    def connect(self):
        return False

    def pay(self,user,purchase_data):
        return False


class test_PaymentSystem(unittest.TestCase):
    def setUp(self) -> None:
        self.payment = PaymentSystem()
    def test_connect(self):
        self.payment.set_external(external_paymentstub())
        self.assertTrue(self.payment.connect())

        self.payment.set_external(failed_paymenstub())
        self.assertFalse(self.payment.connect())

    def test_pay(self):
        self.payment.set_external(failed_paymenstub())
        self.assertListEqual(jsonpickle.decode(self.payment.pay("user",jsonpickle.encode(Cart()))),[])
