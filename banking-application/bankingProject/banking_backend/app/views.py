# views.py
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserCreationForm
from .models import User, Account
from .models import Account, Transaction


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            pin = form.cleaned_data['pin']
            user.pin_hash = hashlib.md5(pin.encode()).digest()
            user.save()
            # Optionally, you can create an account for the user here
            # Account.objects.create(holder=user, name="Savings Account")
            return redirect('login')  # Redirect to login page after registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def account_detail(request, account_uuid):
    account = get_object_or_404(Account, uuid=account_uuid)
    return render(request, 'account_detail.html', {'account': account})

def transaction_detail(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return render(request, 'transaction_detail.html', {'transaction': transaction})
