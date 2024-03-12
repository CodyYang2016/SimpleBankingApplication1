from .Transaction import Transaction

class Account:
    def __init__ (self, name, the_holder, theBank):
        self.name = name
        self.holder = the_holder
        self.uuid = theBank.getNewAccountUUID()
        self.transactions = []

    def getSummaryLine(self):
        balance = self.getBalance()
        if balance >= 0:
            return f"{self.uuid} : ${balance:.2f}: {self.name}"
        else:
            return f"{self.uuid} : $({-balance:.2f}): {self.name}"
    
    def getBalance(self):
        balance = 0
        for t in self.transactions:
            balance += t.amount
        return balance
    
    def printTransHistory(self):
        print(f"\nTransaction history for account {self.uuid}")
        for i in range(len(self.transactions) - 1, -1, -1):
            print(self.transactions[i].getSummaryLine())

    def addTransaction(self, amount, memo):
        newTrans = Transaction(amount, memo, self)
        self.transactions.append(newTrans)
    