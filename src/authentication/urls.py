from django.urls import path
from . import views


app_name = 'authentication'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('register/', views.register_view, name='register'),
    path('edit-profile/', views.edit_view, name='edit-profile'),
    path('change-password/', views.change_password_view, name='change-password')
]
