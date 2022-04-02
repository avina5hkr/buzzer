from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('host/', views.host, name="host"),
    path('player/', views.players, name="players"),
]
