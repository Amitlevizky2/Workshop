import unittest
import jsons
from project.domain_layer.stores_managment.Store import Store

from project.domain_layer.communication_managment.Publisher import Publisher


class publisherStub():
    def purchase_update(self, id, name, user):
        pass
    def store_ownership_update(self,id ,name, user):
        pass

class test_publisher(unittest.TestCase):
    def setUp(self) -> None:
        self.publisher = Publisher(None)
        self.store = Store(0, "test store", "test owner")
        self.store.store_managers = {"Moshe": [],
                                     "Amit": [Store.add_product],
                                     "Hadar": [],
                                     "Lielle": [Store.remove_product],
                                     "Noa": [Store.add_visible_product_discount],
                                     "Evgeny": [Store.update_product]}

        self.standard_users = ["Avishay",
                               "Alex",
                               "Ron"]

    def test_purchase_update(self):
        res= self.publisher.purchase_update(self.store.store_id,self.store.name,self.store.store_owners)
        x=5