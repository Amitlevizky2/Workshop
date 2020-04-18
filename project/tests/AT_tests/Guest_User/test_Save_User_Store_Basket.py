import unittest

from project.tests.AT_tests.test_env.Driver import Driver
from project.tests.AT_tests import ATsetUP


class Save_basket_Store(unittest.TestCase):
    def setUp(self):
        self.service = Driver.make_bridge()
        ATsetUP.setup(self.service)

    def test_save_basket_happy(self): pass

    def test_save_basket_sad(self):
        pass


if __name__ == '__main__':
    unittest.main()
