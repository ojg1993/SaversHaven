from django.urls import path

from address import views

app_name = 'address'

urlpatterns = [
    path('country/', views.CountryView.as_view(), name='country'),
    ]
