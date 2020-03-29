from .Inventory import Inventory
import unittest


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inv = Inventory()

    def tearDown(self) -> None:
        print("in tearDown")

    def test_getx(self):
        self.assertEqual(self.inv.getx(), 1)
        
if __name__ == '__main__':
    unittest.main()
