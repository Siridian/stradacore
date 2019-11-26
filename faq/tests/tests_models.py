"""
This module tests the models of the faq app
"""

from django.test import TestCase
from faq.models import *
import re


class TestTag(TestCase):
    # This class tests the Tag and TagManager models

    @classmethod
    def setUpTestData(cls):
        # Sets up three tags

        cls.footag = Tag.objects.create(name="footag")
        cls.bartag = Tag.objects.create(name="bartag")
        cls.testtag = Tag.objects.create(name="testtag")

    def test_tag_attributes(self):
        # Tests that tag instance attributes are of the correct type

        self.assertTrue(isinstance(self.testtag, Tag))
        self.assertEqual(type(self.testtag.name), str)

    def test_detected_tags(self):
        # Tests that the detect_tags() method of the tag manager works
        string = "tagbarTagbE FFFteSTagfOOTag"
        detected_tags = Tag.objects.detect_tags(string)

        self.assertEqual(type(detected_tags), list)
        self.assertEqual(len(detected_tags), 2)
        self.assertEqual(detected_tags[0], self.footag)
        self.assertEqual(detected_tags[1], self.bartag)


class TestAnswer(TestCase):
    # This class tests the Answer and AnswerManager models

    @classmethod
    def setUpTestData(cls):
        # Sets up three answers and three tags
        cls.testtag1 = Tag.objects.create(name="testtag1")
        cls.testtag2 = Tag.objects.create(name="testtag2")
        cls.testtag3 = Tag.objects.create(name="testtag3")

        cls.testanswerthird = Answer.objects.create(
            title="testanswerthird",
            upload_content="no matching tag",
        )
        cls.testanswersecond = Answer.objects.create(
            title="testanswersecond",
            upload_content="one matching tag",
        )
        cls.testanswerfirst = Answer.objects.create(
            title="testanswerfirst",
            upload_content="two matching tags",
        )

        cls.testanswerthird.tags.add(cls.testtag3)
        cls.testanswersecond.tags.add(cls.testtag1, cls.testtag3)
        cls.testanswerfirst.tags.add(cls.testtag1, cls.testtag2)

    def test_answer_attributes(self):
        # Tests that answer instance attributes are of the correct type
        self.assertTrue(isinstance(self.testanswerfirst, Answer))
        self.assertEqual(type(self.testanswerfirst.title), str)
        self.assertEqual(type(self.testanswerfirst.upload_content), str)

    def test_find_and_sort(self):
        # Tests that the find_and_sort() method of the answer manager works
        tag_list = [self.testtag1, self.testtag2]
        answer_list = Answer.objects.find_and_sort(tag_list)

        self.assertEqual(len(answer_list), 2)
        self.assertEqual(answer_list[0], self.testanswerfirst)
        self.assertEqual(answer_list[1], self.testanswersecond)


class TestQuestion(TestCase):
    # This class tests the Question model

        def test_question_attributes(self):
            # Tests that question instance attributes are of the correct type
            self.testquestion = Question.objects.create(
                content="testcontent",
                mail="test@mail.com"
            )
            regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
            self.assertTrue(isinstance(self.testquestion, Question))
            self.assertEqual(type(self.testquestion.content), str)
            self.assertTrue(re.search(regex, self.testquestion.mail))


class TestQuestion(TestCase):
    # This class tests the Question model

        def test_question_attributes(self):
            # Tests that question instance attributes are of the correct type
            self.testquestion = Question.objects.create(
                content="testcontent",
                mail="test@mail.com"
            )
            regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
            self.assertTrue(isinstance(self.testquestion, Question))
            self.assertEqual(type(self.testquestion.content), str)
            self.assertTrue(re.search(regex, self.testquestion.mail))


class TestAnsweredQuestion(TestCase):
    # This class tests the Question model

        def test_answered_question_attributes(self):
            """
            Tests that answered question instance attributes
            are of the correct type
            """
            self.testanswer = Answer.objects.create(
                title="testtitle",
                upload_content="testcontent"
            )
            self.testaquestion = AnsweredQuestion.objects.create(
                user_question="testcontent",
                validated_answer=self.testanswer
            )
            self.assertTrue(isinstance(self.testaquestion, AnsweredQuestion))
            self.assertEqual(type(self.testaquestion.user_question), str)
            self.assertEqual(
                self.testaquestion.validated_answer,
                self.testanswer
            )
