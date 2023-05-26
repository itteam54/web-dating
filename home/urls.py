from django.urls import path
from . import views

urlpatterns = [
    path('', views.preregister, name='preregister'),
    path('home/', views.postregister, name="index"),
]
