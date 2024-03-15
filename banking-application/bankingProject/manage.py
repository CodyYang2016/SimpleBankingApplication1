#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import bcrypt

def create_customer(first_name, last_name, password):
    # Import Customer model
    from banking_backend.models import customer
    print(first_name, last_name)

    # Create a customer
    pwd_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return customer.objects.create(first_name=first_name, last_name=last_name, password_hash=pwd_hash)

def create_account(customer, name, description, account_type):
    # Import Account model
    from banking_backend.models import Account, AccountType

    # Retrieve or create AccountType
    account_type_obj, _ = AccountType.objects.get_or_create(name=account_type)

    # Create an account
    return Account.objects.create(name=name, customer_id=customer, account_description=description, account_type_id=account_type_obj)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banking_backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banking_backend.settings')
    import django
    django.setup()

    # Run the create_customer function with hardcoded values
    create_customer("John", "Doe", "test1234")
