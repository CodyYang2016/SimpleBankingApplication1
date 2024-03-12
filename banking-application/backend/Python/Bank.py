import random
from .Users import User
from .Account import Account

class Bank:
    def __init__(self, name):
        self.name = name
        self.users = []
        self.accounts = []

    def getNewUserUUID(self):
        while True:
            uuid = ''.join(str(random.randint(0, 9)) for _ in range(6))
            if not any(user.uuid() == uuid for user in self.users):
                return uuid

    def getNewAccountUUID(self):
        while True:
            uuid = ''.join(str(random.randint(0, 9)) for _ in range(12))
            if not any(account.uuid() == uuid for account in self.accounts):
                return uuid

    def addAccount(self, account):
        self.accounts.append(account)

    def addUser(self, first_name, last_name, pin):
        newUser = User(first_name, last_name, pin, self)
        self.users.append(newUser)

        newAccount = Account("Savings", newUser, self)
        newUser.addAccount(newAccount)
        self.addAccount(newAccount)

        return newUser

    def userLogin(self, user_id, pin):
        for user in self.users:
            if user.uuid == user_id and user.validatePin(pin):
                return user
        return None