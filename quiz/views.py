from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import *


def start(request):
    return render(request, 'quiz/start.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('quiz:index')
    else:
        form = UserCreationForm()
    return render(request, 'authorisation/register.html', {'form': form})


@login_required
def index(request):
    latest_test_list = Test.objects.all()[:4]
    context = {'latest_tests_list': latest_test_list}
    return render(request, 'quiz/index.html', context)


@login_required
def detail(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    questions = test.question_set.order_by('id')
    return render(request, 'quiz/detail.html', {'test': test, 'questions': questions})


@login_required
def results(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    questions = test.question_set.order_by('id')
    participant_answers = [record.answer for record in TestParticipantAnswers.objects.filter(test_id=test_id)]
    result = [(question.question_text, answer.answer_text, str(answer.is_correct))
              for question, answer in zip(questions, participant_answers)]
    points = sum(1 if a.is_correct else 0 for a in participant_answers)
    context = {'test': test, 'result': result, 'points': points}
    return render(request, 'quiz/results.html', context)


@login_required
def answer_the_question(request, test_id, question_id):
    ide = int(request.POST['answer'])
    answer = get_object_or_404(Answer, id=ide)
    try:
        test_participant_answer = get_object_or_404(TestParticipantAnswers, test_participant=1, test=test_id,
                                                    question=question_id)

    except:
        test_participant_answer = TestParticipantAnswers(test_participant=get_object_or_404(TestParticipant, id=1),
                                                         test=get_object_or_404(Test, id=test_id),
                                                         question=get_object_or_404(Question, id=question_id),
                                                         answer=get_object_or_404(Answer, id=ide))
        test_participant_answer.save()
        return HttpResponseRedirect(reverse('quiz:detail', args=(test_id,)))

    test_participant_answer.answer = answer
    test_participant_answer.save()
    return HttpResponseRedirect(reverse('quiz:detail', args=(test_id,)))

