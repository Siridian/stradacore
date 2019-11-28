"""
This file contains the url paths for the recipes app
"""

from django.urls import path

from recipes import views

urlpatterns = [
    path(r'landing/', views.landing, name="landing"),
    path(r'recipe_download/<int:recipe_id>',
         views.recipe_download,
         name="recipe_download"
    ),
    path(r'recipe_refresh/', views.recipe_refresh, name="recipe_refresh"),
    path(r'grocery_list/', views.grocery_list, name="grocery_list")
    ]