from project.domain_layer.users_managment.User import User


class RegisteredUser(User):

    def __init__(self, username):
        super().__init__()
        self.username = username
        self.purchase_history = []
        self.loggedin = False



