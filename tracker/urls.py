from django.urls import path

from . import views

urlpatterns = [
    path("dashboard", views.dashboard, name="dashboard"),
    path("wallets", views.wallets, name="wallets"),
    path("createcategory", views.createcategory, name="createcategory"),
    path("addexpense", views.addexpense, name="addexpense"),
    path("history", views.history, name="history")
]
