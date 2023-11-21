from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "account"


urlpatterns = [
    path('', views.login_view, name='login'),
    path('register', views.register, name='register'),
    
    path('logout', views.logout_view, name='logout'),
    path('delete', views.delete_view, name='delete'),
    path('yes', views.yes, name='yes'),
]