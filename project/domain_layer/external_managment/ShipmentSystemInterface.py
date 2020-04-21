class ShipmentSystemInterface:
    def __init__(self):
        self.external = None

    def set_external(self, external_shipment_system):
        self.external = external_shipment_system

    def connect(self):
        if self.external is not None:
            return self.external.connect()
        return False

    def ship(self):
        return self.external.ship()
