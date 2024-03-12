import hashlib
import uuid


class User:
    def __init__(self, firstName, lastName, pin, theBank):
        self.firstName = firstName
        self.lastName = lastName
        self.uuid = str(uuid.uuid4())
        self.pinHash = hashlib.md5(pin.encode()).digest()
        self.accounts = []

        print(f"New account created! First name: {firstName} Last name: {lastName} UUID: {self.uuid}")

    def updateUserInformation(self, newFirstName, newLastName, newPin):
        self.firstName = newFirstName
        self.lastName = newLastName
        self.pinHash = hashlib.md5(newPin.encode()).digest()

    def addAccount(self, newAccount):
        self.accounts.append(newAccount)

    def validatePin(self, pin):
        prospectivePinHash = hashlib.md5(pin.encode()).digest()
        return prospectivePinHash == self.pinHash

    def printAccountsSummary(self):
        print(f"\n\n{self.first_name}'s accounts summary")
        for idx, account in enumerate(self.accounts, 1):
            print(f"  {idx} {account.getSummaryLine()}")

    def printAcctTransHistory(self, acct_idx):
        self.accounts[acct_idx].printTransHistory()

    def addAcctTransaction(self, acct_idx, amount, memo):
        self.accounts[acct_idx].addTransaction(amount, memo)