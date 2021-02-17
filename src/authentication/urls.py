from django.urls import path
from . import views


app_name = 'authentication'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('register/', views.register_view, name='register')
]
