import unittest
import jsonpickle
from project.tests.AT_tests.test_env.Driver import Driver
from project.tests.AT_tests import ATsetUP


class ViewStoreHistory(unittest.TestCase):
    def setUp(self) -> None:
        self.service = Driver.make_bridge()
        self.store_id = ATsetUP.setup(self.service)
        self.service.login("avi", "123")
        products = jsonpickle.decode(self.service.searchProduct("Apple"))
        x=5
        self.service.add_product(self.store_id, products, 3)
        self.service.buy()

    def test_view_store_history_success(self):
        history = self.service.view_store_history(self.store_id)
        x=5
        self.assertIsNotNone(history)
        self.assertEqual("Apple", history[0].products["Apple"][0].name)

    def test_view_store_history_sad(self):

        self.service.logout()
        history = self.service.view_store_history(self.store_id)
        self.assertIsNone(history)



    def test_view_store_history_bad(self):
        history = self.service.view_store_history(self.store_id+40)
        self.assertIsNone(history)


if __name__ == '__main__':
    unittest.main()
