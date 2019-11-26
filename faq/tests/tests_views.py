"""
This module tests the views and utils of the faq app
"""

from django.test import TestCase
from faq.views import *
from faq.utils import create_question


class TestViewIndex(TestCase):
    # This class tests the index view

    def test_index_200(self):
        # Tests that index view returns a 200 code

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)


class TestViewLanding(TestCase):
    # This class tests the landing view

    def test_landing_200(self):
        # Tests that landing view returns a 200 code

        response = self.client.get("/faq/landing/")

        self.assertEqual(response.status_code, 200)


class TestViewMemoList(TestCase):
    # This class tests the memo_list view

    def test_memo_list_200(self):
        # Tests that memo_list view returns a 200 code

        response = self.client.get("/faq/memo_list/")

        self.assertEqual(response.status_code, 200)

    def test_memo_list_context(self):
        # Tests that memo_list returns all memo answers

        memo_tag = Tag.objects.create(name="memo")

        testanswer1 = Answer.objects.create(title="testtitle1")
        testanswer2 = Answer.objects.create(title="testtitle2")
        testanswer3 = Answer.objects.create(title="testtitle3")

        testanswer1.tags.add(memo_tag)
        testanswer3.tags.add(memo_tag)

        response = self.client.get("/faq/memo_list/")

        self.assertEqual(len(response.context["answers"]), 2)
        self.assertEqual(response.context["answers"][0], testanswer1)
        self.assertEqual(response.context["answers"][1], testanswer3)


class TestViewAnswerSearch(TestCase):
    # This class tests the answer_search view

    def test_answer_search_200(self):
        # Tests that memo_list view returns a 200 code

        response = self.client.get("/faq/answer_search/")

        self.assertEqual(response.status_code, 200)

    def test_answer_search_context(self):
        # Tests that answer_search returns sorted answers matching a query

        alpha_tag = Tag.objects.create(name="alpha")
        beta_tag = Tag.objects.create(name="beta")
        gamma_tag = Tag.objects.create(name="gamma")

        testanswer1 = Answer.objects.create(title="testtitle1")
        testanswer2 = Answer.objects.create(title="testtitle2")
        testanswer3 = Answer.objects.create(title="testtitle3")

        testanswer1.tags.add(alpha_tag)
        testanswer2.tags.add(alpha_tag, beta_tag)
        testanswer3.tags.add(gamma_tag)

        testquery = "fOOBetabar+foo+aLPHagama "

        response = self.client.get("/faq/answer_search/",
                                   {"query": testquery}
                                   )

        self.assertEqual(len(response.context["answers"]), 2)
        self.assertEqual(response.context["answers"][0], testanswer2)
        self.assertEqual(response.context["answers"][1], testanswer1)
        self.assertEqual(response.context["tags"], [alpha_tag, beta_tag])
        self.assertEqual(self.client.session['last_query'],
                         "fOOBetabar+foo+aLPHagama "
                         )


class TestViewAnswerDetail(TestCase):
    # This class tests the answer_detail view

    @classmethod
    def SetUpTestData(cls):
        Answer.objects.create(id=1, title="testtitle")

    def test_answer_detail_valid_id(self):
        # Tests that answer_detail returns a 200 code for an existing answer

        response = self.client.get("/faq/answer_detail/1", follow=True)

        self.assertEqual(response.status_code, 200)

    def test_answer_detail_invalid_id(self):
        # Tests that answer_detail returns a 404 code for a non-existing answer

        response = self.client.get("/faq/answer_detail/2/", follow=True)

        self.assertEqual(response.status_code, 404)

    def test_answer_detail_correct_context(self):
        # Tests that answer_detail sends answer's informations through context

        response = self.client.get("/faq/answer_detail/1/", follow=True)

        self.assertEqual(response.context['answer'].title, "testtitle")

    def test_answer_detail_last_query(self):
        # Tests that answer_detail's context contains last user's query

        response = self.client.get("/faq/answer_detail/1/", follow=True)

        self.assertEqual(response.context['last_query'], "none")

        self.client.get("/faq/answer_search/", {"query": "testquery"})
        response = self.client.get("/faq/answer_detail/1", follow=True)

        self.assertEqual(response.context['last_query'], "testquery")
