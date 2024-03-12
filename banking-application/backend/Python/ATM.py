import random
from datetime import datetime
import hashlib
import uuid

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
            if not any(account.uuid == uuid for account in self.accounts):
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
        print(f"\n\n{self.firstName}'s accounts summary")
        for idx, account in enumerate(self.accounts, 1):
            print(f"  {idx} {account.getSummaryLine()}")

    def printAcctTransHistory(self, acct_idx):
        self.accounts[acct_idx].printTransHistory()

    def addAcctTransaction(self, acct_idx, amount, memo):
        self.accounts[acct_idx].addTransaction(amount, memo)
    
    def num_accounts(self):
        return len(self.accounts)
    
    def getAccountBalance(self, acct_idx):
        return self.accounts[acct_idx].getBalance()

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
    

class ATM:
    @staticmethod
    def main():
        # init Scanner
        sc = Scanner()

        # theBank init
        print("What bank would you like to interact with? ")
        bank_name = input()
        the_bank = Bank(bank_name)

        # add a user, which creates a savings account too
        print("What is your first name? ")
        first_name = input()

        print("What is your last name? ")
        last_name = input()

        print("What is your pin? ")
        pin = input()

        # user object
        a_user = the_bank.addUser(first_name, last_name, pin)

        # add a checking account for user
        new_account = Account("Checking", a_user, the_bank)
        a_user.addAccount(new_account)
        the_bank.addAccount(new_account)

        while True:
            # login prompt to stay until successful login
            cur_user = ATM.main_menu_prompt(the_bank, sc)

            # main menu until quit
            ATM.print_user_menu(cur_user, sc)

    @staticmethod
    def main_menu_prompt(the_bank, sc):
        while True:
            print(f"\n\nWelcome to {the_bank.name}\n\n")
            print("Enter user ID: ")
            user_id = input()
            print("Enter pin: ")
            pin = input()

            auth_user = the_bank.userLogin(user_id, pin)
            if auth_user is None:
                print("Incorrect user ID/pin combination. Please try again.")
            else:
                return auth_user

    @staticmethod
    def print_user_menu(the_user, sc):
        while True:
            # print a summary of user's account
            the_user.printAccountsSummary()

            while True:
                print(f"{the_user.firstName}, what would you like to do?")
                print("  1) Show Account Transaction History")
                print("  2) Make a Withdrawal")
                print("  3) Make a Deposit")
                print("  4) Transfer")
                print("  5) Quit")
                print("Enter choice: ")
                choice = int(input())

                if choice < 1 or choice > 5:
                    print("Invalid input: Please choose 1-5")
                else:
                    break

            if choice == 1:
                ATM.show_trans_history(the_user, sc)
            elif choice == 2:
                ATM.withdraw_funds(the_user, sc)
            elif choice == 3:
                ATM.deposit_funds(the_user, sc)
            elif choice == 4:
                ATM.transfer_funds(the_user, sc)
            elif choice == 5:
                print("Thank you for using our services. Goodbye!")
                break  # Exit the function and program

    @staticmethod
    def show_trans_history(the_user, sc):
        while True:
            print(f"Enter the number (1-{the_user.num_accounts()}) of the account whose transactions you want to see: ")
            the_account = int(input()) - 1
            if the_account < 0 or the_account >= the_user.num_accounts():
                print("Invalid Account: Try again")
            else:
                break

        # print the transaction history
        the_user.printAcctTransHistory(the_account)

    @staticmethod
    def transfer_funds(the_user, sc):
        while True:
            print(f"Enter the number (1-{the_user.num_accounts()}) of the account to transfer from: ")
            from_acct = int(input()) - 1
            if from_acct < 0 or from_acct >= the_user.num_accounts():
                print("Invalid Account: Try again")
            else:
                balance = the_user.getAccountBalance(from_acct)
                break

        while True:
            print(f"Enter the number (1-{the_user.num_accounts()}) of the account to transfer to: ")
            to_acct = int(input()) - 1
            if to_acct < 0 or to_acct >= the_user.num_accounts():
                print("Invalid Account: Try again")
            else:
                break

        while True:
            print(f"Enter the amount to transfer (max ${balance}): $")
            amount = float(input())
            if amount < 0:
                print("Amount must be greater than zero.")
            elif amount > balance:
                print(f"Amount must not be greater than balance of ${balance}")
            else:
                break

        the_user.addAcctTransaction(from_acct, -1 * amount, f"Transfer to Account {the_user.accounts[to_acct].uuid}")
        the_user.addAcctTransaction(to_acct, amount, f"Transfer from Account {the_user.accounts[from_acct].uuid}")

    @staticmethod
    def withdraw_funds(the_user, sc):
        while True:
            print(f"Enter the number (1-{the_user.num_accounts()}) of the account to withdraw from: ")
            from_acct = int(input()) - 1
            if from_acct < 0 or from_acct >= the_user.num_accounts():
                print("Invalid Account: Try again")
            else:
                balance = the_user.getAccountBalance(from_acct)
                break

        while True:
            print(f"Enter the amount to withdraw (max ${balance}): $")
            amount = float(input())
            if amount < 0:
                print("Amount must be greater than zero.")
            elif amount > balance:
                print(f"Amount must not be greater than balance of ${balance}")
            else:
                break

        print("Enter a memo: ")
        memo = input()

        the_user.addAcctTransaction(from_acct, -1 * amount, memo)

    @staticmethod
    def deposit_funds(the_user, sc):
        while True:
            print(f"Enter the number (1-{the_user.num_accounts()}) of the account to deposit in: ")
            to_acct = int(input()) - 1
            if to_acct < 0 or to_acct >= the_user.num_accounts():
                print("Invalid Account: Try again")
            else:
                balance = the_user.getAccountBalance(to_acct)
                break

        while True:
            print(f"Enter the amount to deposit (max ${balance}): $")
            amount = float(input())
            if amount < 0:
                print("Amount must be greater than zero.")
            else:
                break

        print("Enter a memo: ")
        memo = input()

        the_user.addAcctTransaction(to_acct, amount, memo)


class Scanner:
    def next_line(self):
        return input()

    def next_int(self):
        return int(input())

    def next_float(self):
        return float(input())


ATM.main()