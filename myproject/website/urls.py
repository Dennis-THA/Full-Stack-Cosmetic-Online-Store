from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('members', views.members, name="members"),
    path('login', views.login_user, name="login"),
    path('signup', views.signup, name="signup"),
    path('success', views.success, name="success"),
]
