from django.urls import path
from . import views

urlpatterns = [
    # my Added routes
    path('', views.home_view, name='n_home'),
    path('login/', views.login_view, name='n_login'),
    path('register/', views.register_view, name='n_register'),
    path('logout/', views.logout_view, name='n_logout'),
    path('profile/', views.profile_view, name='n_profile'),
    path('forgotpassword/', views.forgotpwd_view, name='n_forgotpassword'),
    path('changepassword/', views.changepwd_view, name='n_changepassword'),
]
