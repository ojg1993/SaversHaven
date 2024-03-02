from django.urls import path

from review import views

app_name = 'review'

urlpatterns = [
    path('reviews/', views.ReviewListAPIView.as_view(), name='review-list'),
    path('reviews/<int:id>/', views.ReviewDetailAPIView.as_view(), name='review-detail')
    ]
