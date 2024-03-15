# views.py
from django.shortcuts import render, redirect, get_object_or_404

from .forms import customerCreationForm
from .models import customer, Account
from .models import Account, Transaction
import bcrypt



def register_user(request):
    if request.method == 'POST':
        form = customerCreationForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            pin = form.cleaned_data['pin']
            customer.password_hash = bcrypt.hashpw(pin.encode(), bcrypt.gensalt())
            customer.save()
            # Optionally, you can create an account for the customer here
            # Account.objects.create(holder=customer, name="Savings Account")
            return redirect('login')  # Redirect to login page after registration
    else:
        form = customerCreationForm()
    return render(request, 'register.html', {'form': form})

def account_detail(request, account_uuid):
    account = get_object_or_404(Account, uuid=account_uuid)
    return render(request, 'account_detail.html', {'account': account})

def transaction_detail(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return render(request, 'transaction_detail.html', {'transaction': transaction})
