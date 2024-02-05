from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('account.urls')),
    path('api/address/', include('address.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'),
         name='api-docs'),
]




if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
    	path('__debug__/', include(debug_toolbar.urls))
    ]
