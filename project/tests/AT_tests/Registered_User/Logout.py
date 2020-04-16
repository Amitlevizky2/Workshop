import unittest
from project.tests.AT_tests.test_env.Driver import Driver

class Logout(unittest.TestCase):
    def setUp(self):
        self.service = Driver.make_bridge()


    def test_logout_happy(self):
        self.service.register("user", "pass")
        self.service.login("user", "pass")
        res = self.service.logout("user")
        self.assertTrue(res)

    def test_logout_bad(self):
        res1 = self.service.logout("guestuser")
        self.assertFalse(res1)



if __name__ == '__main__':
    unittest.main()
