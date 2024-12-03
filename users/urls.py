from django.urls import path
from .views import register,loginView
urlpatterns = [
    path('register/', register.as_view()),
    path('login/', loginView.as_view())

]







