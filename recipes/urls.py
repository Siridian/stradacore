"""
This file contains the url paths for the recipes app
"""

from django.urls import path

from recipes import views

urlpatterns = [
    path(r'landing/', views.landing, name="landing"),
    path(r'recipes_search/', views.recipes_search, name="recipes_search"),
    ]