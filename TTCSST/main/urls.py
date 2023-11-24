from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("allocations", views.allocations, name="allocations"),
    path("history", views.history, name="history")
]