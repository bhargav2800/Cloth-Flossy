from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('',views.home, name="home"),
    path('login_user/', views.loginPage, name="login-user"),
    path('logout_user/', views.logoutUser, name="logout-user"),
    path('register_user/', views.register_customer, name="register-user"),
    path('register_brand/', views.register_brand, name="register-brand"),
    path('user_profile/', views.user_profile, name="user-profile")
]