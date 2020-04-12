from project import service_layer


class UserManager:

    security = service_layer.Security()
    incremental_id = 0

    def __init__(self):
        self.reg_user_list = {}
        self.guest_user_list = {}
        ##maybe dictionary {id, username}
        self.admins = []
