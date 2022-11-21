from django.urls import path
from .views import UsersView

urlpatterns = [
    path('home', UsersView.as_view()),
]
