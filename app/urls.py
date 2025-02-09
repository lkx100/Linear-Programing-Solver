from django.urls import path
from .views import transportation_method, graphical_method, simplex_method, home

urlpatterns = [
    path('', home, name='home'),
    path('transportation_method/', transportation_method, name='transportation_method'),
    path('graphical_method/', graphical_method, name='graphical_method'),
    path('simplex_method/', simplex_method, name='simplex_method'),
]
