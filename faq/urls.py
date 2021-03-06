"""
This file contains the url paths for the faq app
"""


from django.urls import path

from faq import views

urlpatterns = [
    path(r'landing/', views.landing, name="landing"),
    path(r'memo_list/', views.memo_list, name="memo_list"),
    path(r'answer_search/', views.answer_search, name="answer_search"),
    path(r'answer_detail/<int:answer_id>', views.answer_detail, name="answer_detail"),
    path(r'answer_validate/', views.answer_validate, name="answer_validate"),
    path(r'question_ask/', views.question_ask, name="question_ask"),
    path(r'ml_info/', views.ml_info, name="ml_info"),
    ]
