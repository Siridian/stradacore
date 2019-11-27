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
    )
    ]