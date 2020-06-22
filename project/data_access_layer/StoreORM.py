from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from project.data_access_layer import Base, session, engine, proxy
from project.data_access_layer.ManagerORM import ManagerORM
from project.data_access_layer.ManagerPermissionORM import ManagerPermissionORM
from project.data_access_layer.OwnerORM import OwnerORM
#from project.data_access_layer.RegisteredUserORM import association_owners, association_managers
# from project.data_access_layer.RegisteredUserORM import association_owners, association_managers
from project.data_access_layer.DiscountORM import DiscountORM
from project.data_access_layer.PurchaseORM import PurchaseORM


def find_store(store_id):
    return proxy.get_session().query(StoreORM).filter_by(store_id=store_id).first()



class StoreORM(Base):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    discount_index = Column(Integer)
    purchase_index = Column(Integer)
    owned_by = relationship("OwnerORM", back_populates="store")
    managed_by = relationship("ManagerORM")
    discounts = relationship("DiscountORM")
    policies = relationship("PolicyORM")

    def add(self):
        Base.metadata.create_all(engine, [Base.metadata.tables['stores']], checkfirst=True)
        proxy.get_session().add(self)
        proxy.get_session().commit()

    def appoint_owner(self,  appointed_by,owner):
        Base.metadata.create_all(engine, [Base.metadata.tables['stores']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['owners']], checkfirst=True)
        Base.metadata.create_all(engine, [Base.metadata.tables['regusers']], checkfirst=True)

        owner = OwnerORM(username=owner, store_id=id, appointed_by=appointed_by)
        self.owned_by.append(owner)
        proxy.get_session().add(owner)
        proxy.get_session().commit()

    def remove_owner(self, to_remove):
        self.remove_appointed_by(to_remove)
        proxy.get_session().query(OwnerORM).delete.where(username=to_remove)
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
        proxy.get_session().query(ManagerORM).delete.where(username=to_remove)
        proxy.get_session().commit()

    def add_permission(self, manager, permission):
        perm = ManagerPermissionORM(username=manager, store_id=self.id, permission=permission)
        perm.add()

    def remove_permission(self, manager, permission):
        proxy.get_session().query(ManagerPermissionORM).delete.where(username=manager, store_id=self.id, permission=permission)
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
        for manager in self.managed_by:
            name = manager.username
            appointed_by[manager.appointed_by].append(name)
            permissions = proxy.get_session().query(ManagerPermissionORM).filter_by(username=name)
            managers[name] = []
            for permission in permissions:
                managers[name].append(permission)
        store.store_managers = managers
        discounts = {}
        for discount in self.discounts:
            dis = None
            if discount.discriminator == 'Visible Discount':
                from project.data_access_layer import VisibleProductDiscountORM
                dis = proxy.get_session().query(VisibleProductDiscountORM).filter_by(discount_id=discount.discount_id)
            elif discount.discriminator == 'Conditional Product':
                from project.data_access_layer import ConditionalProductDiscountORM
                dis = proxy.get_session().query(ConditionalProductDiscountORM).filter_by(discount_id=discount.discount_id)
            elif discount.discriminator == 'Conditional Store':
                from project.data_access_layer.ConditionalStoreDiscountORM import ConditionalStoreDiscountORM
                dis = proxy.get_session().query(ConditionalStoreDiscountORM).filter_by(discount_id=discount.discount_id)
            elif discount.discriminator == 'Composite Discount':
                from project.data_access_layer.CompositeDiscountORM import CompositeDiscountORM
                dis = proxy.get_session().query(CompositeDiscountORM).filter_by(discount_id=discount.discount_id)
            discounts[discount.discount_id]=dis.createObject()
        store.discounts = discounts
        ## inventory
        from project.data_access_layer.ProductORM import ProductORM
        inventory = {}
        products = proxy.get_session().query(ProductORM).filter_by(store_id=self.id)
        for product in products:
            prod = product.createObject()
            inventory[product.name] = prod
        store.inventory.products = inventory
        policies = {}
        for policy in self.policies:
            pol = None
            if policy.discriminator == 'Product Policy':
                from project.data_access_layer import ProductPolciesORM
                pol = proxy.get_session().query(ProductPolciesORM).filter_by(policy_id=policy.policy_id)
            elif policy.discriminator == 'Store Policy':
                from project.data_access_layer.StorePolicyORM import StorePolicyORM
                pol = proxy.get_session().query(StorePolicyORM).filter_by(policy_id=policy.policy_id)
            elif policy.discriminator == 'Composite Policy':
                from project.data_access_layer.CompositePolicyORM import CompositePolicyORM
                pol = proxy.get_session().query(CompositePolicyORM).filter_by(policy_id=policy.policy_id)
            policies[policy.policy_ic] = pol.createObject()
        store.purchase_policies = policies
        return store
