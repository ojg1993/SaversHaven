from dj_rest_auth.registration.views import VerifyEmailView
from django.urls import re_path

from user import views

app_name = 'user'

urlpatterns = [
    re_path(
        r'^registration/account-verify-email/$',
        VerifyEmailView.as_view(),
        name='account_email_verification_sent'
    ),
    re_path(
        r'^registration/account-confirm-email/(?P<key>[-:\w]+)/$',
        views.ConfirmEmailView.as_view(),
        name='account_confirm_email'
    ),
]
