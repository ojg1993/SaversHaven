from django.urls import include, path
from rest_framework.routers import DefaultRouter

from transaction import views

router = DefaultRouter()
# router.register('transactions', views.TransactionViewSet)


app_name = 'transaction'

urlpatterns = [
    path('', include(router.urls)),
    ]
