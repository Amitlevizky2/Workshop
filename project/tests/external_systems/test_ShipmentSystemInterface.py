import unittest

from project.domain_layer.external_managment.ShipmentSystemInterface import ShipmentSystemInterface


class external_shipmentstub:
    def connect(self):
        return True

    def ship(self):
        return True


class failed_shipmentstub:
    def connect(self):
        return False

    def ship(self):
        return False


class test_ShipmentSystemInterface(unittest.TestCase):
    def setUp(self) -> None:
        self.shipment = ShipmentSystemInterface()

    def test_connect(self):
        self.shipment.set_external(external_shipmentstub())
        self.assertTrue(self.shipment.connect())

        self.shipment.set_external(failed_shipmentstub())
        self.assertFalse(self.shipment.connect())
    def test_ship(self):
        self.shipment.set_external(external_shipmentstub())
        self.assertTrue(self.shipment.ship())

        self.shipment.set_external(failed_shipmentstub())
        self.assertFalse(self.shipment.ship())
