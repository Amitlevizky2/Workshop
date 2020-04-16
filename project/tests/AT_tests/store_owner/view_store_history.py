import unittest

from project.tests.AT_tests.test_env.Driver import Driver
from project.tests.AT_tests import ATsetUP


class ViewStoreHistory(unittest.TestCase):
    def setUp(self) -> None:
        self.service = Driver.make_bridge()
        self.store_id = ATsetUP.setup(self.service)
        self.service.add_product(self.store_id, ATsetUP.products[0], 3)
        self.service.buy()

    def test_view_store_history_success(self):
        history = self.service.view_store_history(self.store_id)
        self.assertIsNotNone(history)
        self.assertEqual("Apple", history.products[0].product_name)

    def test_view_store_history_sad(self):

        self.service.logout()
        history = self.service.view_store_history(self.store_id)
        self.assertIsNone(history)



    def test_view_store_history_bad(self):
        history = self.service.view_store_history(self.store_id+40)
        self.assertIsNone(history)


if __name__ == '__main__':
    unittest.main()
