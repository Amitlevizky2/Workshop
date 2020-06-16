from unittest import TestCase

from project.domain_layer.users_managment.RegisteredUser import RegisteredUser

class TestRegisteredUser(TestCase):
    def setUp(self) -> None:
        self.reg_user = RegisteredUser("user1")

    def test_logout(self):
        self.reg_user.logout()
        self.assertFalse(self.reg_user.loggedin)

    def test_login(self):
        self.reg_user.login()
        self.assertTrue(self.reg_user.loggedin)

    def test_view_purchase_history(self):
        pass

    def test_get_managed_store(self):
        pass

    def test_add_managed_store(self):
        self.reg_user.managed_stores.clear()
        self.reg_user.add_managed_store(1234)
        self.assertEqual(self.reg_user.managed_stores.pop(0), 1234)
