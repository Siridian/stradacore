"""
The views of the faq app handles core features (such as index page)
as well as the search engine and detailed page of the Answers
"""

from django.shortcuts import render


def index(request):
    # Displays home page
    return render(request, 'faq/index.html')


def answer_list(request):
    pass


def answer_search(request):
    pass


def answer_detail(request):
    pass
