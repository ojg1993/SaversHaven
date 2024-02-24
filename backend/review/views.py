from django.db.models import Q
from rest_framework import generics, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Review, DirectTransaction
from review.serializers import ReviewSerializer


class ReviewListAPIView(generics.ListAPIView):
    '''View for listing user's reviews'''
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        # Custom queryset to filter reviews based on the current user

        current_user = self.request.user
        # filter transactions where the current user is either the buyer or the seller
        user_reviews = (
                Q(transaction__chatroom__buyer=current_user) |
                Q(transaction__chatroom__seller=current_user))

        # Filter review objects based on the defined query
        reviews = Review.objects.filter(user_reviews)
        return reviews


class ReviewCreateAPIView(generics.CreateAPIView):
    '''View for creating a review'''
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        transaction = DirectTransaction.objects.get(id=self.kwargs.get('id'))
        reviewer = request.user
        receiver = transaction.chatroom.buyer \
            if reviewer == transaction.chatroom.seller \
            else transaction.chatroom.seller

        data = {
            'transaction': transaction.id,
            'reviewer': reviewer.id,
            'receiver': receiver.id,
            'review': request.data['review'],
            'rating': request.data['rating']
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
            return Response({'message': 'Review sent.'},
                            status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailAPIView(generics.RetrieveAPIView):
    '''View for retrieving review details'''
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'id'
