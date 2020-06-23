import unittest
from project.tests.AT_tests.test_env.Driver import Driver
import os
from project.data_access_layer import Base, meta, engine


class Login(unittest.TestCase):

    def setUp(self):
        self.service = Driver.make_bridge()
        self.service.register("username","password")


    def tearDown(self) -> None:
        self.drop_table('stores')
        self.drop_table('baskets')
        self.drop_table('CompositeDiscounts')
        self.drop_table('CompositePolicies')
        self.drop_table('conditionalproductdiscounts')
        self.drop_table('conditionalstorediscounts')
        self.drop_table('discounts')
        self.drop_table('to_apply_composite')
        self.drop_table('managers')
        self.drop_table('managerpermissions')
        self.drop_table('owners')
        self.drop_table('Policy_in_composite')
        self.drop_table('policies')
        self.drop_table('predicates')
        self.drop_table('products')
        self.drop_table('productspolicies')
        self.drop_table('productsinbaskets')
        self.drop_table('Discount_products')
        self.drop_table('Policy_products')
        self.drop_table('productsinpurcases')
        self.drop_table('purchases')
        self.drop_table('passwords')
        self.drop_table('regusers')
        self.drop_table('stores')
        self.drop_table('storepolicies')
        self.drop_table('notifications')
        self.drop_table('visibleProductDiscounts')

    def drop_table(self, table_name: str):
        if table_name in Base.metadata.tables:
            Base.metadata.drop_all(engine, [Base.metadata.tables[table_name]])

    def test_happy_registration(self):
        res1 = self.service.login("username", "password")
        self.assertTrue(res1)

    def test_sad_registration(self):
        res1 = self.service.login("userNotName", "password")
        self.assertTrue(res1['error'])

    def test_bad_registration(self):
        result1 = self.service.login("", "password")
        self.assertIsNotNone(result1)

    # @classmethod
    # def tearDownClass(cls):
    #     os.remove("C:\\Users\\Owner\\Desktop\\Sadna_project\\Workshop\\daldal.db")


if __name__ == '__main__':
    unittest.main()
