from datetime import datetime
class Transaction:

    # initiate transaction without memo
    def __init__ (self, amount, newAccount):
        self.amount = amount
        self.timeStamp = datetime.now()
        self.inAccount = newAccount
        self.memo = ""

    # initiate transaction with memo
    def __init__ (self, amount, newMemo, newAccount):
        self.amount = amount
        self.timeStamp = datetime.now()
        self.inAccount = newAccount
        self.memo = newMemo
    
    def getSummaryLine(self):
        if self.amount >= 0:
            return "{}: ${:.02f}: {}".format(self.timeStamp, self.amount, self.memo)
        else:
            return "{}: $({:.02f}): {}".format(self.timeStamp, -self.amount, self.memo)