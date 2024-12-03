from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register.as_view()),
    path('login/', loginView.as_view()),
    path('user/', userget.as_view()),
    path('logout/',logoutView.as_view())



]







