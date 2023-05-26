from django.urls import path, include
from . import views
from profiles import url_reset

urlpatterns = [
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('create-profile/', views.create_profile, name='create_profile'),
    path('verification-message/', views.verification_message, name="verification_message"),
    path('member/<id>/', views.member_profile, name='member_profile'),
    path('password-reset/', include(url_reset)),
    path('account/', views.account, name='account'),
]
