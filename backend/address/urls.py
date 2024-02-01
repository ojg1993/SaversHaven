from django.urls import path, include
from rest_framework.routers import DefaultRouter
from address import views

router = DefaultRouter()
router.register('countries', views.CountryViewSet)
router.register('counties', views.CountyViewSet)
router.register('cities', views.CityViewSet)

app_name = 'address'

urlpatterns = [
    path('', include(router.urls)),
    ]
