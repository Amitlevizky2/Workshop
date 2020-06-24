
import unittest
import transaction
from project.service_layer.ExternalserviseAPI import ExternalServiceAPI

class test_API(unittest.TestCase):
    def setUp(self):
        self.api = ExternalServiceAPI()

    def bytes_to_int(self,bytes):
        result = 0

        for b in bytes:
            result = result * 256 + int(b)

        return result
    def test_pay(self):
        try:
            res = self.api.pay(4234234234,12,2019,"hadar",455,132321)
            self.recipt = int(res.content)
            if 10000 <= self.recipt <= 100000:
                transaction.commit()
            self.assertNotEquals(self.recipt,-1)
        except:
            transaction.abort()


    def test_cansel_pay(self):
        try:
            res = self.api.pay(4234234234, 12, 2019, "hadar", 455, 132321)
            self.recipt1 = int(res.content)
            x=5
            if 10000 <= self.recipt1 <= 100000:
                res = self.api.cancelpay(res.content)
                print( "pay: ",self.recipt1)
                print("cansle pay: ",int(res.content))

                self.assertEqual(res, 1)
            transaction.commit()
        except:
            transaction.abort()

    def test_supply(self):
        try:

            res = self.api.supply("hadar","betshemesh","jerusalem","israel",423432)
            self.recipt = int(res.content)
            if 10000 <= self.recipt <= 100000:
                transaction.commit()
            self.assertNotEquals(self.recipt, -1)
        except:
            transaction.abort()