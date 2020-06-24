import datetime
from datetime import datetime, date

from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean, update
from sqlalchemy.exc import SQLAlchemyError

from project.data_access_layer import Base, session, engine, proxy



class StatsORM(Base):
    __tablename__ = 'stats'
    date = Column(String, primary_key=True)
    guests = Column(Integer)
    reg_users = Column(Integer)
    managers = Column(Integer)
    owners = Column(Integer)

    def add(self):
        try:
            Base.metadata.create_all(engine, [Base.metadata.tables['stats']], checkfirst=True)
            proxy.get_session().add(self)
            proxy.get_session().commit()
        except:
            session.rollback()


    def update_guest(self):
        self.guests += 1
        proxy.get_session().commit()

    def reduce_guest(self):
        self.guests -= 1
        proxy.get_session().commit()

    def update_reg_users(self):
        self.reg_users += 1
        proxy.get_session().commit()

    def update_managers(self):
        self.managers += 1
        proxy.get_session().commit()

    def update_owner(self):
        self.owners += 1
        proxy.get_session().commit()


