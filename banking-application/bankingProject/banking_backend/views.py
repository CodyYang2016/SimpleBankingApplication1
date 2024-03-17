from rest_framework import viewsets, status
from .models import customer, Account, Transaction
from .serializers import CustomerSerializer, AccountSerializer, TransactionSerializer
from rest_framework.response import Response


class CustomerViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing customer instances.
    """
    serializer_class = CustomerSerializer
    queryset = customer.objects.all()
    def create(self, request, *args, **kwargs):
        mutable_data = request.data.copy()  # Create a mutable copy of the request data
        serializer = self.get_serializer(data=mutable_data)
        if serializer.is_valid():
            # Extract data from serializer
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            email = serializer.validated_data.get('email')
            raw_password = serializer.validated_data.get('password')

            # Create and save the customer instance
            new_customer = customer.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            new_customer.set_password(raw_password)
            new_customer.save()

            # Return success response
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Return error response if serializer is not valid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing account instances.
    """
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

class TransactionViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing transaction instances.
    """
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
