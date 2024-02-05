from django.urls import include, path
from rest_framework.routers import DefaultRouter

from product import views

router = DefaultRouter()
router.register('categories', views.CategoryListViewSet)
router.register('categories', views.CategoryDetailViewSet)

app_name = 'product'

urlpatterns = [
    path('', include(router.urls))
    ]
