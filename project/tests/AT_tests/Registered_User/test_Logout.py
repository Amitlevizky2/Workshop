import unittest
from project.tests.AT_tests.test_env.Driver import Driver

class Logout(unittest.TestCase):
    def setUp(self):
        self.service = Driver.make_bridge()


    def test_logout_happy(self):
        self.service.register("user", "pass")
        self.service.login("user", "pass")
        res = self.service.logout()
        self.assertTrue(res)

    def test_logout_bad(self):
        res2 = None
        if not self.service.out:
            res2 = self.service.logout()
        self.assertIsNone(res2)



if __name__ == '__main__':
    unittest.main()
