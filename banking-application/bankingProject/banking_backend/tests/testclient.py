print("Client has entered test")


import os
import sys
import django
from django.test import TestCase


# Set up Django environment settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bankingProject.settings')

# Initialize Django settings
django.setup()

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ))
sys.path.append(parent_dir)

from banking_backend.models import customer, Account, AccountType, Transaction, TransactionType
from django.utils import timezone
import bcrypt

class CustomerModelTests(TestCase):

    def test_create_customer(self):
        print ("Testing Customer Creation")
        # Create a test customer
        pwd_hash = bcrypt.hashpw('test1234'.encode(), bcrypt.gensalt())
        cust = customer(first_name='John', last_name='Doe', password=pwd_hash)
        cust.save()

        # Retrieve the customer and verify details
        retrieved = customer.objects.get(first_name='John', last_name='Doe')
        self.assertEqual(retrieved.first_name, 'John')
        self.assertTrue(bcrypt.checkpw('test1234'.encode(), retrieved.password))
        print ("Customer created and retrieved succesfully")


class AccountModelTests(TestCase):

    def setUp(self):
        # This method will run before each test function in this class
        AccountType.objects.get(name='Savings')
        customer.objects.create(first_name='Jane', last_name='Doe')

    def test_create_account(self):
        # Create a test account
        cust = customer.objects.get(first_name='Jane')
        acc_type = AccountType.objects.get(name='Savings')
        account = Account(name='Jane Savings', customer=cust, account_id='123e4567-e89b-12d3-a456-426614174010', account_description='Jane\'s savings account', account_type_id=acc_type)
        account.save()

        # Verify the account details
        retrieved = Account.objects.get(name='Jane Savings')
        self.assertEqual(retrieved.account_description, "Jane's savings account")

class TransactionModelTests(TestCase):

    def setUp(self):
        # Set up required objects
        AccountType.objects.create(name='Checking')
        cust = customer.objects.create(first_name='Bob', last_name='Smith', customer_id='123e4567-e89b-12d3-a456-426614174002')
        self.account = Account.objects.create(name='Bob Checking', customer=cust, account_id='123e4567-e89b-12d3-a456-426614174011', account_description='Bob\'s checking account', account_type_id=AccountType.objects.get(name='Checking'))

    def test_create_transaction(self):
        # Create and save a new transaction
        transaction = Transaction(amount=100.00, memo='Deposit', in_account=self.account)
        transaction.save()

        # Verify the transaction details
        retrieved = Transaction.objects.get(memo='Deposit')
        self.assertEqual(retrieved.amount, 100.00)
        self.assertEqual(retrieved.in_account, self.account)

