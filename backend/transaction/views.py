from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import DirectTransaction
from transaction.serializers import DirectTransactionSerializer


class DirectTransactionViewSet(viewsets.ModelViewSet):
    '''Creating & Processing direct transaction status '''
    serializer_class = DirectTransactionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = DirectTransaction.objects.all()

    def get_queryset(self):
        # Custom queryset to filter transactions based on the current user
        current_user = self.request.user
        # filter transactions where the current user is either the buyer or the seller
        user_transactions = (Q(chatroom__buyer=current_user) |
                             Q(chatroom__seller=current_user))
        # Filter DirectTransaction objects based on the defined query
        transactions = DirectTransaction.objects.filter(user_transactions)
        return transactions
