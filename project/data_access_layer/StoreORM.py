from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship, with_polymorphic, polymorphic_union

from project.data_access_layer import Base, session, engine, proxy
from project.data_access_layer.ManagerORM import ManagerORM
from project.data_access_layer.ManagerPermissionORM import ManagerPermissionORM
from project.data_access_layer.OwnerORM import OwnerORM
#from project.data_access_layer.RegisteredUserORM import association_owners, association_managers
# from project.data_access_layer.RegisteredUserORM import association_owners, association_managers

from project.data_access_layer.PurchaseORM import PurchaseORM
from project.data_access_layer.ConditionalProductDiscountORM import ConditionalProductDiscountsORM
from project.data_access_layer.ConditionalStoreDiscountORM import ConditionalStoreDiscountORM
from project.data_access_layer.VisibleProductDiscountORM import VisibleProductDiscountORM
from project.data_access_layer.CompositeDiscountORM import CompositeDiscountORM

def find_store(store_id):
    return proxy.get_session().query(StoreORM).filter_by(store_id=store_id).first()



class StoreORM(Base):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    discount_idx = Column(Integer)
    purchases_idx = Column(Integer)
    owned_by = relationship("OwnerORM", back_populates="store")
    managed_by = relationship("ManagerORM")
   # discounts = relationship("DiscountORM")
    vis = relationship("VisibleProductDiscountORM")
    condprod = relationship("ConditionalProductDiscountsORM")
    condstore = relationship("ConditionalStoreDiscountORM")
    comp= relationship("CompositeDiscountORM")
    policies = relationship("PolicyORM")

    def add(self):
        try:
            Base.metadata.create_all(engine, [Base.metadata.tables['stores']], checkfirst=True)
            proxy.get_session().add(self)
            proxy.get_session().commit()
        except SQLAlchemyError as e:
            session.rollback()
            error = str(type(e))
            # print(error)
            return error



    def appoint_owner(self, appointed_by, owner):
        Base.metadata.create_all(engine, [Base.metadata.tables['stores']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['owners']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['regusers']], checkfirst=True)

        owner = OwnerORM(username=owner, store_id=id, appointed_by=appointed_by)
        self.owned_by.append(owner)
        proxy.get_session().add(owner)
        proxy.get_session().commit()

    def remove_owner(self, to_remove):
        self.remove_appointed_by(to_remove)
        res = proxy.get_session().query(OwnerORM).filter_by(username=to_remove).first()
        proxy.get_session().delete(res)
        proxy.get_session().commit()

    def remove_appointed_by(self, to_remove):
        owners = proxy.get_session().query(OwnerORM).filter_by(appointed_by=to_remove)
        for owner in owners:
            owner.remove()
        managers = proxy.get_session().query(OwnerORM).filter_by(appointed_by=to_remove)
        for manager in managers:
            manager.remove()
        proxy.get_session().commit()

    def remove_manager(self, to_remove):
        self.remove_appointed_by(to_remove)
        res = proxy.get_session().query(ManagerORM).filter_by(username=to_remove).first()
        res.remove()
        proxy.get_session().commit()

    def add_permission(self, manager, permission):
        perm = ManagerPermissionORM(username=manager, store_id=self.id, permission=permission)
        perm.add()

    def remove_permission(self, manager, permission):
        res = proxy.get_session().query(ManagerPermissionORM).filter_by(username=manager, store_id=self.id, permission=permission).first()
        proxy.get_session().delete(res)
        proxy.get_session().commit()

    def appoint_manager(self, owner, to_appoint):
        Base.metadata.create_all(engine, [Base.metadata.tables['managers']], checkfirst=True)
        manager = ManagerORM(username=to_appoint, store_id=id, appointed_by=owner)
        self.managed_by.append(manager)
        proxy.get_session().add(manager)
        proxy.get_session().commit()

    def getPurchases(self):
        return proxy.get_session().query(PurchaseORM).filter_by(store_id=id)


    def createObject(self):
        from project.domain_layer.stores_managment.Store import Store
        store = Store(self.id, self.name, self.owned_by[0].username, self)
        store.discount_idx = self.discount_idx
        store.purchases_idx = self.purchases_idx
        owners = []
        appointed_by = {}
        Base.metadata.create_all(engine, [Base.metadata.tables['owners']], checkfirst=True)
        for owner in self.owned_by:
            owners.append(owner.username)
            if owner.username not in appointed_by.keys():
                appointed_by[owner.username] = []
            if owner.appointed_by not in appointed_by.keys():
                if owner.appointed_by is not '':
                    appointed_by[owner.appointed_by]=[owner.username]
            else:
                appointed_by[owner.appointed_by].append(owner.username)
        store.store_owners = owners
        Base.metadata.create_all(engine, [Base.metadata.tables['managers']], checkfirst=True)
        managers = {}
        for manager in self.managed_by:
            name = manager.username
            appointed_by[manager.appointed_by].append(name)
            Base.metadata.create_all(engine, [Base.metadata.tables['managerpermissions']], checkfirst=True)
            permissions = proxy.get_session().query(ManagerPermissionORM).filter_by(username=name)
            managers[name] = []
            for permission in permissions:
                managers[name].append(permission.permission)
        store.store_managers = managers
        store.appointed_by =appointed_by
        discounts = {}
        # print(dis)
        Base.metadata.create_all(engine, [Base.metadata.tables['visibleProductDiscounts']], checkfirst=True)
        for discount in self.vis:
            discounts[discount.discount_id] = discount.createObject()
        Base.metadata.create_all(engine, [Base.metadata.tables['conditionalproductdiscounts']], checkfirst=True)
        for discount in self.condprod:
            discounts[discount.discount_id] = discount.createObject()
        Base.metadata.create_all(engine, [Base.metadata.tables['conditionalstorediscounts']], checkfirst=True)
        for discount in self.condstore:
            discounts[discount.discount_id] = discount.createObject()
        Base.metadata.create_all(engine, [Base.metadata.tables['CompositeDiscounts']], checkfirst=True)
        for discount in self.comp:
            discounts[discount.discount_id] = discount.createObject()
        store.discounts = discounts
        ## inventory
        from project.data_access_layer.ProductORM import ProductORM
        inventory = {}
        Base.metadata.create_all(engine, [Base.metadata.tables['products']], checkfirst=True)
        products = proxy.get_session().query(ProductORM).filter_by(store_id=self.id)
        for product in products:
            prod = product.createObject()
            inventory[product.name] = prod
        store.inventory.products = inventory
        policies = {}
        Base.metadata.create_all(engine, [Base.metadata.tables['policies']], checkfirst=True)
        for policy in self.policies:
            policies[policy.policy_id] = policy.createObject()
        store.purchase_policies = policies
        Base.metadata.create_all(engine, [Base.metadata.tables['purchases']], checkfirst=True)
        orms = proxy.get_handler_session().query(PurchaseORM).filter_by(store_id=self.id)
        purchases = []
        for p in orms:
            purchase = p.createObject()
            purchases.append(purchase)
        store.sales = purchases
        return store
