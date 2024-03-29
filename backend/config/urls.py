from dj_rest_auth.views import PasswordResetConfirmView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from rest_framework.decorators import api_view
from rest_framework.response import Response

from user import views

@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint to ensure the application is running properly.
    Returns a simple 200 OK response.
    """
    return Response({"message": "Server running"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', health_check, name='health_check'),

    # Apps
    path('api/auth/', include('user.urls')),
    path('api/address/', include('address.urls')),
    path('api/product/', include('product.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/transaction/', include('transaction.urls')),
    path('api/review/', include('review.urls')),

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

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
