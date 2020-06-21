from project import logger
from project.service_layer.ExternalserviseAPI import ExternalServiceAPI


class ShipmentSystemInterface:
    def __init__(self):
        self.external = None
        self.EX = ExternalServiceAPI()

    def set_external(self, external_shipment_system):
        self.external = external_shipment_system

    def connect(self):
        if self.external is not None:
            x = str(self.EX.connect())
            if x == "OK":
                #logger.error("Failed to connect to shipment system")
                return True
        return False

    def ship(self,name,address,city,country,zip):
        return self.EX.supply(name,address,city,country,zip)
