from project.service_layer.StoresManagerInterface import StoresManagerInterface
import unittest


class test_StoresManagerInterface(unittest.TestCase):
    def setUp(self):
        self.store_manager_interface = StoresManagerInterface(None)

    def test_search_product(self):
        pass

    def test_get_store(self):
        self.store_manager_interface.get_store(0)
        pass

