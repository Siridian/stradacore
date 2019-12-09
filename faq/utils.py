"""
This file contains utility functions for the faq app,
such as the create_question function, that mails a specified address
when a new question is created
"""

from django.core.mail import send_mail
from django.template.loader import render_to_string

from faq.models import Question
from django.conf import settings


def create_question(content, mail):
    question = Question.objects.create(content=content, mail=mail)
    send_mail(
        "Nouvelle question posée sur astradadiucore.fr",
        render_to_string("faq/mail_content.txt"),
        settings.EMAIL_HOST_USER,
        settings.NOTIFIED_TARGET
    )
    return question
