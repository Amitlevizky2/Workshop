from unittest import TestCase

from project.data_access_layer import proxy, session



class TestCart(TestCase):
    def setUp(self) -> None:
        self.proxy = proxy

    def test_real_proxy(self):
        sess = session
        self.assertEqual(self.proxy.get_session(),sess)

    def test_fail_proxy(self):
        proxy.session = False
        self.assertFalse(proxy.get_session())
        proxy.session = session