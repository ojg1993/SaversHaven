from django.urls import path

from user import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'user'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.TokenLoginView.as_view(), name='login'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
