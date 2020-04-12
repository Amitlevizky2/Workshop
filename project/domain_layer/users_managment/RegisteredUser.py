from project.domain_layer.users_managment.User import User


class RegisteredUser(User):

    def __init__(self, username):
        super().__init__()
        self.username = username
        self.purchase_history = []
        self.loggedin = False


    def view_purchase_history(self):
        return self.purchase_history

    def loggout(self):
        self.loggedin = False

    def login(self):
        self.loggedin = True


