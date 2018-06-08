from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404
from .models import *
from django.shortcuts import render, get_object_or_404


def index(request):
    latest_test_list = Test.objects.all()[:4]
    context = {'latest_tests_list': latest_test_list}
    return render(request, 'quiz/index.html', context)


def detail(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    questions = test.question_set.order_by('id')
    return render(request, 'quiz/detail.html', {'test': test, 'questions': questions})


def results(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    questions = test.question_set.order_by('id')
    participant_answers = [record.answer for record in TestParticipantAnswers.objects.filter(test_id=test_id)]
    result = [(question.question_text, answer.answer_text, str(answer.is_correct))
              for question, answer in zip(questions, participant_answers)]
    points = sum(1 if a.is_correct else 0 for a in participant_answers)
    context = {'test': test, 'result': result, 'points': points}
    return render(request, 'quiz/results.html', context)

