import unittest
import os

import jsons

from project.data_access_layer import Base, engine
from project.tests.AT_tests import ATsetUP
from project.tests.AT_tests.test_env.Driver import Driver
from project.tests.domain_layer.stores_managment.test_Store import PublisherStub


class test_add_policies_and_discounts(unittest.TestCase):
    def setUp(self) -> None:
        self.service = Driver.make_bridge()
        self.service.bound_publisher(PublisherStub(None))
        ATsetUP.setup(self.service)
        self.service.register("aaa", "password")
        self.service.login("aaa", "password")

    def test_add_product_policy_success(self):
        res = self.service.add_purchase_product_policy(0, 'avi', 2, 10, ['Apple', 'Banana'])
        res = jsons.loads(res)
        self.assertFalse(res['error'])

        self.service.add_product(0, 'Banana', 9)
        res = self.service.buy(458053299887,12,2022,"amit levizky",448,2957474,"rager","beersheva","israel",283443)
        self.assertFalse(res['error'])
        res = self.service.get_purchase_history()
        res = jsons.loads(res)
        self.assertFalse(res['error'])

    def test_add_product_policy_sad(self):
        res = self.service.add_purchase_product_policy(0, 'aviv', 2, 10, ['Apple', 'Banana'])
        res = jsons.loads(res)
        self.assertTrue(res['error'])

    def test_add_product_policy_bad(self):
        res = self.service.add_purchase_product_policy(0, 'avi', 11, 10, [None])
        res = jsons.loads(res)
        self.assertTrue(res['error'])



    def test_add_store_policy_success(self):
        res = self.service.add_purchase_store_policy(0,'avi',2,10)
        res = jsons.loads(res)
        self.assertFalse(res['error'])

        self.service.add_product(0, 'Banana', 9)
        res = self.service.buy(458053299887,12,2022,"amit levizky",448,2957474,"rager","beersheva","israel",283443)
        self.assertFalse(res['error'])
        res = self.service.get_purchase_history()
        res = jsons.loads(res)
        self.assertFalse(res['error'])

    def test_add_store_policy_sad(self):
        res = self.service.add_purchase_store_policy(0,'aviv',2,10)
        res = jsons.loads(res)
        self.assertFalse(res['ans'])

    def test_add_store_policy_bad(self):
        res = self.service.add_purchase_store_policy(0,'avi',12,10)
        res = jsons.loads(res)
        self.assertTrue(res['error'])

    def test_visiable_discount_product_success(self):
        res = self.service.add_visible_discount_to_product(0,'avi',"2018-11-12","2022-11-12",50,['Apple','Banana'])
        res = jsons.loads(res)
        self.assertFalse(res['error'])

        self.service.add_product(0, 'Banana', 5)
        res = self.service.buy(458053299887,12,2022,"amit levizky",448,2957474,"rager","beersheva","israel",283443)
        self.assertFalse(res['error'])
        res = self.service.get_purchase_history()
        res = jsons.loads(res)
        self.assertEqual(50,res['data'][0]['0']['products']['Banana']['price_after_disc'])


    def test_visiable_discount_product_sad(self):
        res = self.service.add_visible_discount_to_product(0,'aviv',"2018-11-12","2022-11-12",50,['Apple','Banana'])
        res = jsons.loads(res)
        self.assertTrue(res['error'])

        self.service.add_product(0, 'Banana', 5)
        res = self.service.buy(458053299887, 12, 2022, "amit levizky", 448, 2957474, "rager", "beersheva", "israel",
                               283443)
        self.assertFalse(res['error'])
        res = self.service.get_purchase_history()
        res = jsons.loads(res)
        self.assertEqual(100, res['data'][0]['0']['products']['Banana']['price_after_disc'])

    def test_visiable_discount_product_bad(self):
        res = self.service.add_visible_discount_to_product(0, 'aviv', "2033-11-12", "2022-11-12", 50,
                                                           ['Apple', 'Banana'])
        res = jsons.loads(res)
        self.assertTrue(res['error'])

        self.service.add_product(0, 'Banana', 5)
        res = self.service.buy(458053299887, 12, 2022, "amit levizky", 448, 2957474, "rager", "beersheva", "israel",
                               283443)
        self.assertFalse(res['error'])
        res = self.service.get_purchase_history()
        res = jsons.loads(res)
        self.assertEqual(100, res['data'][0]['0']['products']['Banana']['price_after_disc'])

    def test_conditional_discount_store_success(self):
        res = self.service.add_conditional_discount_to_store(0, 'avi', "2018-11-12", "2022-11-12", 50,20)

        res = jsons.loads(res)
        self.assertFalse(res['error'])

        self.service.add_product(0, 'Banana', 5)
        res = self.service.buy(458053299887, 12, 2022, "amit levizky", 448, 2957474, "rager", "beersheva", "israel",
                               283443)
        self.assertFalse(res['error'])
        res = self.service.get_purchase_history()
        res = jsons.loads(res)
        self.assertFalse(res['error'])

    def test_conditional_discount_store_sad(self):
        res = self.service.add_conditional_discount_to_store(0, 'aviv', "2018-11-12", "2022-11-12", 50, 20)

        res = jsons.loads(res)
        self.assertTrue(res['error'])

        self.service.add_product(0, 'Banana', 5)
        res = self.service.buy(458053299887, 12, 2022, "amit levizky", 448, 2957474, "rager", "beersheva", "israel",
                               283443)
        self.assertFalse(res['error'])
        res = self.service.get_purchase_history()
        res = jsons.loads(res)
        self.assertFalse(res['error'])

    def test_conditional_discount_store_bad(self):
        res = self.service.add_conditional_discount_to_store(0, 'avi', "2033-11-12", "2022-11-12", 50, 20)

        res = jsons.loads(res)
        self.assertTrue(res['error'])

        self.service.add_product(0, 'Banana', 5)
        res = self.service.buy(458053299887, 12, 2022, "amit levizky", 448, 2957474, "rager", "beersheva", "israel",
                               283443)
        self.assertFalse(res['error'])
        res = self.service.get_purchase_history()
        res = jsons.loads(res)
        self.assertFalse(res['error'])

    def test_composite_success(self):
        res1 = self.service.add_visible_discount_to_product(0,'avi',"2018-11-12","2022-11-12",50,['Apple','Banana'])
        res1 = jsons.loads(res1)
        res1 = res1['data']['discount_id']
        res2 = self.service.add_visible_discount_to_product(0,'avi',"2018-11-12","2022-11-12",20,['Apple','Banana'])
        res2 = jsons.loads(res2)
        res2 = res2['data']['discount_id']
        res = self.service.add_composite_discount(0, 'avi', "2018-11-12", "2022-11-12", "or", {res1: ['Banana','Apple']},[res2])

        res = jsons.loads(res)
        self.assertFalse(res['error'])

        self.service.add_product(0, 'Banana', 5)
        res = self.service.buy(458053299887, 12, 2022, "amit levizky", 448, 2957474, "rager", "beersheva", "israel",
                               283443)
        self.assertFalse(res['error'])
        res = self.service.get_purchase_history()
        res = jsons.loads(res)
        self.assertFalse(res['error'])

    def ttest_composite_sad(self):
        res = self.service.add_composite_discount(0, 'aviv', "2018-11-12", "2022-11-12", "or")

        res = jsons.loads(res)
        self.assertTrue(res['error'])

        self.service.add_product(0, 'Banana', 5)
        res = self.service.buy(458053299887, 12, 2022, "amit levizky", 448, 2957474, "rager", "beersheva", "israel",
                               283443)
        self.assertFalse(res['error'])
        res = self.service.get_purchase_history()
        res = jsons.loads(res)
        self.assertFalse(res['error'])

    def test_composite_bad(self):
        res = self.service.add_conditional_discount_to_store(0, 'avi', "2033-11-12", "2022-11-12", 50, 20)

        res = jsons.loads(res)
        self.assertTrue(res['error'])

        self.service.add_product(0, 'Banana', 5)
        res = self.service.buy(458053299887, 12, 2022, "amit levizky", 448, 2957474, "rager", "beersheva", "israel",
                               283443)
        self.assertFalse(res['error'])
        res = self.service.get_purchase_history()
        res = jsons.loads(res)
        self.assertFalse(res['error'])


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
        self.drop_table('regusers')
        self.drop_table('stores')
        self.drop_table('storepolicies')
        self.drop_table('passwords')
        self.drop_table('notifications')
        self.drop_table('visibleProductDiscounts')
        # self.drop_table('stores')

    @classmethod
    def tearDownClass(cls):
        os.remove('/Users/avivlevitzky/PycharmProjects/Workshop/project/tests/test.db')

    def drop_table(self, table_name: str):
        if table_name in Base.metadata.tables:
            Base.metadata.drop_all(engine, [Base.metadata.tables[table_name]])