from project.domain_layer.users_managment.RegisteredUser import RegisteredUser


class Admin(RegisteredUser):

    def __init__(self, username):
        super.__init__(username)

