from Inventory import Inventory

class Store():
    def __init__(self,id,name,store_owner):
        self.id = id
        self.name = name
        self.inventory = Inventory()
        self.sale_policy = None
        self.discount_policy = None
        self.store_owners = [store_owner]
        self.rate = 0