from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session, engine
from project.data_access_layer.ManagerORM import ManagerORM
from project.data_access_layer.ManagerPermissionORM import ManagerPermissionORM
from project.data_access_layer.OwnerORM import OwnerORM
#from project.data_access_layer.RegisteredUserORM import association_owners, association_managers
# from project.data_access_layer.RegisteredUserORM import association_owners, association_managers
from project.data_access_layer.DiscountORM import DiscountORM
from project.data_access_layer.PurchaseORM import PurchaseORM


def find_store(store_id):
    return session.query(StoreORM).filter_by(store_id=store_id).first()



class StoreORM(Base):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    discount_index = Column(Integer)
    purchase_index = Column(Integer)
    owned_by = relationship("OwnerORM", back_populates="store")
    managed_by = relationship("ManagerORM", back_populates="manages")
    discounts = relationship("DiscountORM")


    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['stores']], checkfirst=True)
        session.add(self)
        session.commit()

    def appoint_owner(self, owner, appointed_by):
        Base.metadata.create_all(engine, [Base.metadata.tables['stores']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['owners']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['regusers']], checkfirst=True)

        owner = OwnerORM(username=owner, store_id=id, appointed_by=appointed_by)
        self.owned_by.append(owner)
        session.add(owner)
        session.commit()

    def remove_owner(self, to_remove):
        self.remove_appoint_by(to_remove)
        session.query(OwnerORM).delete.where(username=to_remove)
        session.commit()

    def remove_appointed_by(self, to_remove):
        owners = session.query(OwnerORM).filter_by(appointed_by=to_remove)
        for owner in owners:
            owner.remove()
        managers = session.query(OwnerORM).filter_by(appointed_by=to_remove)
        for manager in managers:
            manager.remove()
        session.commit()

    def remove_manager(self, to_remove):
        self.remove_appoint_by(to_remove)
        session.query(ManagerORM).delete.where(username=to_remove)
        session.commit()

    def add_permission(self, manager, permission):
        perm = ManagerPermissionORM(username=manager, store_id=self.id, permission=permission)
        perm.add()

    def remove_permission(self, manager, permission):
        session.query(ManagerPermissionORM).delete.where(username=manager, store_id=self.id, permission=permission)
        session.commit()

    def appoint_manager(self, owner, to_appoint):
        Base.metadata.create_all(engine, [Base.metadata.tables['managers']], checkfirst=True)
        manager = ManagerORM(username=to_appoint, store_id=id, appointed_by=owner)
        self.managed_by.append(manager)
        session.add(manager)
        session.commit()

    def getPurchases(self):
        return session.query(PurchaseORM).filter_by(store_id=id)


    def createObject(self):
        from project.domain_layer.stores_managment.Store import Store
        store = Store(self.id, self.name, self.owned_by[0].username)
        store.discount_idx = self.discount_index
        store.purchases_idx = self.purchase_index
        owners = []
        appointed_by = {}
        for owner in self.owned_by:
            owners.append(owner.username)
            if owner.username not in appointed_by.keys():
                appointed_by[owner.username] = []
            if owner.appointed_by not in appointed_by.keys():
                appointed_by[owner.appointed_by]=[owner.username]
            else:
                appointed_by[owner.appointed_by].append(owner.username)
        store.store_owners = owners
        managers = {}
        for manager in self.managers:
            name = manager.username
            appointed_by[manager.appointed_by].append(name)
            permissions = session.query(ManagerPermissionORM).filter_by(username=name)
            for permission in permissions:
                managers[name].append(permission)
        store.store_managers = managers
        discounts = {}
        for discount in self.discounts:
            discounts[discount.id]=discount.createObject()
        store.discounts = discounts
        ## inventory
        from project.data_access_layer.ProductORM import ProductORM
        inventory = {}
        products = session.query(ProductORM).filter_by(store_id=self.id)
        for product in products:
            prod = product.createObject()
            inventory[product.name] = prod
        store.inventory.products = inventory
        return store
