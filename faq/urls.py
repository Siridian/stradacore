from django.conf.urls import url
from django.urls import path

from faq import views

urlpatterns = [

    path(r'answer_list/', views.answer_list, name="answer_list"),
    path(r'answer_search/', views.answer_search, name="answer_search"),
    path(r'answer_detail/', views.answer_detail, name="answer_detail"),
    ]
