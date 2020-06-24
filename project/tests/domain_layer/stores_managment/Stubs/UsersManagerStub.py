from project.domain_layer.users_managment.UsersManager import UsersManager


class UsersManagerStub(UsersManager):

    def __init__(self):
        super().__init__(None)

    def add_managed_store(self, username, store_id):
        return True, 'aa'

