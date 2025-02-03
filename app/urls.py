from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('transportation_method/', views.transportation_method, name='transportation_method'),
    path('graphical_method/', views.graphical_method, name='graphical_method'),
]
