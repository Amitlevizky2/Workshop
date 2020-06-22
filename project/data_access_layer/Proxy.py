

class Proxy:
    def __init__(self, session):
        self.session = session

    def get_session(self):
        try:
            # Try to get the underlying session connection, If you can get it, its up
            connection = self.session.connection()
            return self.session
        except:
            return False

    def get_handler_session(self):
        try:
            # Try to get the underlying session connection, If you can get it, its up
            connection = self.session.connection()
            return self.session
        except:
            return False