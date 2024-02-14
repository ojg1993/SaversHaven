from dj_rest_auth.views import PasswordResetConfirmView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from user import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Apps
    path('api/address/', include('address.urls')),
    path('api/product/', include('product.urls')),
    path('api/auth/', include('user.urls')),

    # Authentication
    path("api/auth/", include('dj_rest_auth.urls')),
    path('api/auth/google/login/', views.google_login, name='google_login'),
    path('api/auth/google/login/callback/',
         views.google_callback,
         name='google_callback'
         ),
    path('api/auth/google/login/finish/',
         views.GoogleLogin.as_view(),
         name='google_login_todjango'
         ),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/auth/password/reset/confirm/<uid64>/<token>/',
         PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'
         ),

    # DRF Sepctacular
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'),
         name='api-docs'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
                       path('__debug__/', include(debug_toolbar.urls))
                   ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
