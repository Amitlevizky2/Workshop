import unittest

from project.domain_layer.stores_managment.Store import Store
from project.domain_layer.stores_managment.StoresManager import StoresManager


class test_StoresManager(unittest.TestCase):
    def setUp(self) -> None:
        self.stores_manager = StoresManager()
        self.stores_manager.stores[0] = Store(0, "t_store", "moshe")

    def test_get_store(self):
        with self.assertRaises(ValueError):
            self.stores_manager.get_store(-1)

        self.assertTrue(0 == self.stores_manager.get_store(0).id)


if __name__ == '__main__':
    unittest.main()
