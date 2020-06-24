import unittest

import jsons

from project.tests.AT_tests.test_env.Driver import Driver
from project.tests.AT_tests import ATsetUP


class ViewStoreHistory(unittest.TestCase):
    def setUp(self) -> None:
        self.service = Driver.make_bridge()
        self.store_id = ATsetUP.setup(self.service)
        self.service.login("avi", "123")
        products = self.service.searchProduct("Apple")
        self.service.add_product(self.store_id, "Apple", 3)
        self.service.buy(458053299887,12,2022,"amit levizky",448,2957474,"rager","beersheva","israel",283443)

    def test_view_store_history_success(self):
        history = jsons.load(self.service.view_store_history(self.store_id))
        x=3
        self.assertIsNotNone(history)
        x=5
        self.assertIn("Apple", history['data'][0]['products'].keys())

    def test_view_store_history_sad(self):

        self.service.logout()
        history = jsons.load(self.service.view_store_history(self.store_id))
        self.assertIsNone(history)



    def test_view_store_history_bad(self):
        history =self.service.view_store_history(self.store_id+40)
        self.assertNotIn(self.store_id,history)


if __name__ == '__main__':
    unittest.main()
