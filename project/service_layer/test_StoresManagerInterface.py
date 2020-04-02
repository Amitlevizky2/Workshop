from project.service_layer.StoresManagerInterface import StoresManagerInterface
import unittest


class test_StoresManagerInterface(unittest.TestCase):
    def setUp(self):
        self.store_manager_interface = StoresManagerInterface()

    def test_search_product(self):
        assert False

    def test_get_store(self):
        self.store_manager_interface.get_store(0)

