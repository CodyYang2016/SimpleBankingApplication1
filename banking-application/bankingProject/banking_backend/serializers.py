from rest_framework import serializers
from .models import customer, AccountType, Account, TransactionType, Transaction, Session
import base64
from django.contrib.auth.hashers import make_password, check_password


class CustomerSerializer(serializers.ModelSerializer):
    raw_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password = serializers.CharField(read_only=True)

    class Meta:
        model = customer
        fields = ['first_name', 'last_name', 'customer_id', 'email', 'raw_password', 'password']

    def create(self, validated_data):
        raw_password = validated_data.pop('raw_password', None)
        customer = customer.objects.create(**validated_data)
        if raw_password is not None:
            #customer.set_password(raw_password)
            hashed_password = make_password(raw_password)
            customer.password = hashed_password      
            customer.save()    
        return customer

    def to_representation(self, instance):
        # Ensure that password is represented as a base64-encoded string
        representation = super().to_representation(instance)
        # representation['raw_password'] = base64.b64encode(instance.password).decode('utf-8')
        #representation.pop('raw_password')  # Remove raw_password from the serialized output        
        return representation

    def to_internal_value(self, data):
        # Ensure that password is decoded from base64-encoded string to bytes
        if 'raw_password' in data:
            data['raw_password'] = base64.b64decode(data['raw_password'])
        return super().to_internal_value(data)
    
class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = ['account_type_id', 'name']

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['customer_id', 'account_id', 'account_description', 'account_type_id', 'account_number']

class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = ['transaction_type_id', 'name']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_id', 'timestamp', 'in_account', 'memo', 'account_type_id']

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['session_id', 'customer', 'token', 'expiry_timestamp', 'created_by', 'updated_by', 'create_date', 'last_update']