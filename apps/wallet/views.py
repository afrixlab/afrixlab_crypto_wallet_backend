from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer

@api_view(['GET'])
def wallet_detail(request, user_id):
    wallet = Wallet.objects.get(owner_id=user_id)
    serializer = WalletSerializer(wallet)
    return Response(serializer.data)

@api_view(['POST'])
def create_transaction(request, user_id):
    sender_wallet = Wallet.objects.get(owner_id=user_id)
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        recipient_username = serializer.validated_data['recipient_username']
        amount = serializer.validated_data['amount']
        recipient_wallet = Wallet.objects.get(owner__username=recipient_username)
        try:
            Transaction.objects.create(sender_wallet=sender_wallet, recipient_wallet=recipient_wallet, amount=amount)
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'success': False, 'error_message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
