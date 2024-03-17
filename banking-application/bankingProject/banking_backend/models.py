#models.py
from django.db import models
import hashlib
import uuid
import bcrypt
from .func import generate_account_number
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password


class customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    customer_id = models.AutoField(primary_key=True)
    password = models.BinaryField()
    email = models.EmailField()

    def set_password(self, raw_password):

        hashed_password = make_password(raw_password)
        # self.password = bytes(hashed_password, encoding='utf-8')
        self.password = hashed_password.encode('utf-8')  # Encode the hashed password to bytes

    def check_password(self, raw_password):
       # Check if the given raw password matches the hashed password.

        return check_password(raw_password, self.password.decode('utf-8'))

    def update_customer_information(self, new_first_name, new_last_name, new_password):
        self.first_name = new_first_name
        self.last_name = new_last_name
        self.set_password(new_password) 

    def validate_pin(self, pin):
        return bcrypt.checkpw(pin.encode(), self.password)
    
    class Meta:
        db_table = 'customer'
        managed = False

class AccountType(models.Model):
    account_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'AccountType'
        managed = False


class Account(models.Model):
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    account_id = models.AutoField(primary_key=True)
    account_description = models.CharField(max_length = 1000)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)  # Assuming you've created AccountType model
    account_number = generate_account_number("2326", 10)

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
        db_table = 'account'
        managed = False


class TransactionType(models.Model):
    transaction_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'TransactionType'
        managed = False

class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    in_account = models.ForeignKey(Account, on_delete=models.CASCADE)
    memo = models.CharField(max_length=100)
    account_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)  # Assuming you've created AccountType model


    def get_summary_line(self):
        if self.amount >= 0:
            return f"{self.timestamp}: ${self.amount:.2f}: {self.memo}"
        else:
            return f"{self.timestamp}: $({-self.amount:.2f}): {self.memo}"
    
    class Meta:
        db_table = 'transaction'
        managed = False

class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey('customer', on_delete=models.CASCADE)  # Adjust the relation based on your customer model class name
    token = models.CharField(max_length=64, unique=True)
    expiry_timestamp = models.DateTimeField()
    created_by = models.ForeignKey('customer', related_name='session_created_by', on_delete=models.CASCADE)
    updated_by = models.ForeignKey('customer', related_name='session_updated_by', on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'Session'
        managed = False



