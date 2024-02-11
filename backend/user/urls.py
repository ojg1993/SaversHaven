from django.urls import path, include

from dj_rest_auth.views import PasswordResetConfirmView

app_name = 'user'

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("registeration/", include("dj_rest_auth.registration.urls")),
    path('password/rest/confirm/<uid64>/token/', PasswordResetConfirmView.as_view(), name='password_reset_confirm')

    # path('register/', views.RegisterView.as_view(), name='register'),
    # path('login/', views.TokenLoginView.as_view(), name='login'),
    #
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
