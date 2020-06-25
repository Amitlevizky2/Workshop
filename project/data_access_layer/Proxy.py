from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker


class Proxy:
    def __init__(self, session):
        self.session = session

    def get_session(self):
        try:
            # Try to get the underlying session connection, If you can get it, its up
            connection = self.session.connection()
            return self.session
        except Exception as e:
            self.session.rollback()
            error = str(e.__dict__)
            print(error)
            return 404

    def get_handler_session(self):
        try:
            # Try to get the underlying session connection, If you can get it, its up
            connection = self.session.connection()
            return self.session
        except:
            self.session.rollback()
