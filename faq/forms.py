"""
Contains the faq app's forms, such as the question form,
used by the users to send a question to the admins.
"""

from django.forms import ModelForm, TextInput, EmailInput

from .models import Question


class QuestionForm(ModelForm):
    """
    The question form contains a required text field in which the user writes
    the question, and an optional email field where the user can write their
    mail address
    """

    class Meta:
        model = Question
        fields = ["content", "mail"]
        widget = {
            'content': TextInput(attrs={'class': 'form-control'}),
            'mail': EmailInput(attrs={'class': 'form-control'})
        }
