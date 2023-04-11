from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView, name='home'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]