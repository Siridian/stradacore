"""
The views of the faq app handles core features (such as index page)
as well as the search engine and detailed page of the Answers
"""

from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail

from .models import Answer, Tag, Question


def index(request):
    # Displays home page
    return render(request, 'faq/index.html')


def memo_list(request):
    answers = Answer.objects.filter(tags__name__icontains="memo")
    context = {
        'answers': answers
    }
    return render(request, 'faq/list_memo.html', context)


def answer_search(request):
    query = request.GET.get('query')

    query.replace("+", " ")

    processed_query = query.split()

    selected_list = []

    if not query:
        answers_list = Answer.objects.all()

    else:

        detected_tags = []

        for word in processed_query:

            for tag in Tag.objects.all():

                if tag.name.lower() in word.lower():
                    detected_tags.append(tag)

        for tag in detected_tags:
            selected_list.extend(Answer.objects.filter(tags__name__icontains=tag))

        refined_list = []

        for selectedQuestion in selected_list:
            check = any(tuple[0] == selectedQuestion.id for tuple in refined_list)
            if check:
                targeted_tuple = next(tuple for tuple in refined_list if tuple[0] == selectedQuestion.id)
                retrieved_weight = targeted_tuple[1] + 1
                refined_list.append((selectedQuestion.id, retrieved_weight))
                refined_list.remove(targeted_tuple)
            else:
                refined_list.append((selectedQuestion.id, 0))

        final_list = []

        for refinedQuestion in sorted(refined_list, key=lambda tuple: tuple[1], reverse=True):
            final_list.append(Answer.objects.get(id=refinedQuestion[0]))

        answers_list = final_list

    paginator = Paginator(answers_list, 7)
    page = request.GET.get('page')
    try:
        answers = paginator.page(page)
    except PageNotAnInteger:
        answers = paginator.page(1)
    except EmptyPage:
        answers = paginator.page(paginator.num_pages)

    title = "Résultats pour la requête %s" % query

    context = {
        'answers': answers,
        'title': title,
        'paginate': True
    }

    return render(request, 'faq/list_answer.html', context)


def answer_detail(request):
    pass
