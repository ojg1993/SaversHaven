from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    # Google auth
    # path('google/login123/', views.google_login, name='google_login'),
    # path('google/login123/callback123/', views.google_callback, name='google_callback'),
    # path('google/login/finish/', views.GoogleLogin.as_view(), name='google_login_todjango'),
]
