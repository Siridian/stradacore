"""
This file contains the url paths for the videos app
"""


from django.urls import path

from videos import views

urlpatterns = [
    path(r'landing/', views.landing, name="landing"),
    ]