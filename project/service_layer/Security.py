import hashlib, binascii, os

from project.data_access_layer.SecurityORM import SecurityORM
from project.data_access_layer import SecurityORM as SORM

class Security:

    def __init__(self):
        self.passwords = {str: str}


    def hash_password(self, password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                      salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    def verify_password(self, username, provided_password):
        """Verify a stored password against one provided by user"""
        # if username in self.passwords.keys():
        #     stored_password = self.passwords[username]
        #     salt = stored_password[:64]
        #     stored_password = stored_password[64:]
        #     pwdhash = hashlib.pbkdf2_hmac('sha512',
        #                                   provided_password.encode('utf-8'),
        #                                   salt.encode('ascii'),
        #                                   100000)
        #     pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        #     return pwdhash == stored_password
        # else:
        #     return False
        password = SORM.find_pass(username)
        if self.hash_password(provided_password) == password:
            return True
        else:
            return False

    def add_user(self, username, password):
        self.passwords[username] = self.hash_password(password)
        orm = SecurityORM(username=username, hashed_pass=self.passwords[username])
        orm.add()
