"""
The views of the faq app handle core features (such as index page)
as well as the search engine and detailed page of the Answers
"""

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from faq.forms import QuestionForm, ParagraphErrorList
from .models import Answer, Tag, AnsweredQuestion
from .utils import create_question


def index(request):
    # Displays home page
    return render(request, 'faq/index.html')


def landing(request):
    # Displays faq app home page
    return render(request, 'faq/faq_landing.html')


def memo_list(request):
    # Displays a list of answers tagged as 'memo'
    answers = Answer.objects.filter(tags__name__icontains="memo")
    context = {
        'answers': answers
    }
    return render(request, 'faq/memo_list.html', context)


def answer_search(request):
    """
    Detects tags a in a user query
    and displays associated answers sorted by relevance
    """
    query = request.GET.get('query')
    request.session['last_query'] = query

    context = {
        'paginate': True,
        'form': QuestionForm(),
    }

    if not query:
        answer_list = Answer.objects.all()

    else:
        detected_tags = Tag.objects.detect_tags(query.split("+"))
        answer_list = Answer.objects.find_and_sort(detected_tags)
        context['tags'] = detected_tags

    paginator = Paginator(answer_list, 7)
    page = request.GET.get('page')
    try:
        answers = paginator.page(page)
    except PageNotAnInteger:
        answers = paginator.page(1)
    except EmptyPage:
        answers = paginator.page(paginator.num_pages)

    context['answers'] = answers

    return render(request, 'faq/answer_list.html', context)


def answer_detail(request, answer_id):
    """
    Displays the detailed content of an answer,
    specified through its primary key
    """
    answer = get_object_or_404(Answer, id=answer_id)
    form = QuestionForm()
    last_query = request.session.get('last_query', 'none')

    context = {
        "answer": answer,
        "form": form,
        "answer_id": answer_id,
        "last_query": last_query, }

    return render(request, 'faq/answer_detail.html', context)


def answer_validate(request):
    """
    Ajax view that creates an answered question
    from the current answer page and last user's query
    """
    if request.method == 'POST':
        user_question = request.POST.get("user_question")
        validated_answer = Answer.objects.get(pk=request.POST.get("answer_id"))
        AnsweredQuestion.objects.create(
            user_question=user_question,
            validated_answer=validated_answer
        )
        return HttpResponse('')


def question_ask(request):
    # Creates a Question object in db, using a Question Form
    if request.method == 'POST':
        form = QuestionForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            content = form.cleaned_data['content']
            mail = form.cleaned_data['mail']
            create_question(content, mail)
            context = {
                'content': content,
                'mail': mail,
            }

            return render(request, 'faq/question_confirm.html', context)

        else:
            return redirect(request.META['HTTP_REFERER'])

    else:
        return redirect("faq:landing")
