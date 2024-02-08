from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.TokenLoginView.as_view(), name='login'),
]
