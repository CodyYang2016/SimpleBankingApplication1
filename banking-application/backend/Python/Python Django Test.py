#ATM/models.py
from django.db import models
import hashlib
import uuid

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    uuid = models.UUIDField(unique=True)
    pin_hash = models.BinaryField()


    def update_user_information(self, newFirstName, newLastName, newPin):
        self.first_name = newFirstName
        self.last_name = newLastName
        self.pin_hash = hashlib.md5(newPin.encode()).digest()

    def validate_pin(self, pin):
        prospective_pin_hash = hashlib.md5(pin.encode()).digest()
        return prospective_pin_hash == self.pin_hash

class Account(models.Model):
    name = models.CharField(max_length=100)
    holder = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default =uuid.uuid4, unique=True)

    def get_balance(self):
        balance = 0
        for transaction in self.transaction_set.all():
            balance += transaction.amount
        return balance
    
    def print_transaction_history(self):
        print(f"\nTransaction history for account {self.uuid}")
        for transaction in self.transaction_set.all().order_by('-timestamp'):
            print (transaction.get_summary_line())
    
    def add_transaction(self, amount, memo):
        Transaction.objects.create(amount=amount, memo=memo, account = self)


class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    in_account = models.ForeignKey(Account, on_delete=models.CASCADE)
    memo = models.TextField()

    def get_summary_line(self):
        if self.amount >= 0:
            return f"{self.timestamp}: ${self.amount:.2f}: {self.memo}"
        else:
            return f"{self.timestamp}: $({-self.amount:.2f}): {self.memo}"


