#ATM/models.py
from django.db import models
import hashlib
import uuid
import bcrypt



class customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    customer_id = models.UUIDField(unique=True)
    password_hash = models.BinaryField()


    def update_customer_information(self, newFirstName, newLastName, newPin):
        self.first_name = newFirstName
        self.last_name = newLastName
        self.password_hash = bcrypt.hashpw(newPin.encode(), bcrypt.gensalt())

    def validate_pin(self, pin):
        return bcrypt.checkpw(pin.encode(), self.password_hash)
    
    class Meta:
        db_table = 'retail_banking.customer'
        managed = False

class Account(models.Model):
    name = models.CharField(max_length=100)
    customer_id = models.ForeignKey(customer, on_delete=models.CASCADE)
    account_id = models.UUIDField(default =uuid.uuid4, unique=True)
    account_description = models.CharField(max_length = 1000)
    account_type_id = models.ForeignKey(AccountType, on_delete=models.CASCADE)  # Assuming you've created AccountType model

    def get_balance(self):
        balance = 0
        for transaction in self.transaction_set.all():
            balance += transaction.amount
        return balance
    
    def print_transaction_history(self):
        print(f"\nTransaction history for account {self.uuid}")
        for transaction in self.transaction_set.all().order_by('-timestamp'):
            print (transaction.get_summary_line())
    
    def update_account_description(self, description):
        self.account_description = description


    def add_transaction(self, amount, memo):
        Transaction.objects.create(amount=amount, memo=memo, account = self)

    class Meta:
        db_table = 'retail_banking.account'
        managed = False

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
    
    class Meta:
        db_table = 'retail_banking.transaction'
        managed = False


