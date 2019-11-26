"""
This module tests the forms of the faq app
"""

from django.test import TestCase
from faq.forms import *


class TestQuestionForm(TestCase):
    # This class tests the question form

    def test_form_valid(self):
        # Tests that form is valid with correct data
        data = {"content": "testcontent", "mail": "test@mail.com"}
        form = QuestionForm(data=data)
        self.assertTrue((form.is_valid()))

    def test_form_content_required(self):
        # Tests that form is not valid when no content is given
        data = {"mail": "test@mail.com"}
        form = QuestionForm(data=data)
        self.assertFalse((form.is_valid()))

    def test_form_incorrect_mail(self):
        # Tests that form is not valid when incorrect email is given
        data = {"content": "testcontent", "mail": "testmail.com"}
        form = QuestionForm(data=data)
        self.assertFalse((form.is_valid()))


