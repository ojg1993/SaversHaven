from django.urls import include, path
from rest_framework.routers import DefaultRouter

from review.views import ReviewCreateAPIView
from transaction import views

router = DefaultRouter()
router.register('direct-transactions',
                views.DirectTransactionViewSet,
                basename='direct-transaction')


app_name = 'transaction'

urlpatterns = [
    path('', include(router.urls)),
    path('transactions/<int:id>/review/',
         ReviewCreateAPIView.as_view(),
         name='review-create')
    ]
