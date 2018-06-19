from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
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


def question(request, test_id, question_id):
    test = get_object_or_404(Test, pk=test_id)
    question = get_object_or_404(Question, pk=question_id)
    next_question = test.question_set.filter(id__gt=question.id).order_by('id').first()
    return render(request, 'quiz/question.html', {'test': test, 'question': question, 'next_question': next_question})


@login_required
def index(request):
    latest_test_list = Test.objects.all()[:4]
    context = {'latest_tests_list': latest_test_list}
    return render(request, 'quiz/index.html', context)


@login_required
def detail(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    questions = test.question_set.order_by('id')
    try:
        test_participant = TestParticipant.objects.get(test=test, user=request.user)
    except ObjectDoesNotExist:
        test_participant = TestParticipant(test=test, user=request.user)
    finally:
        test_participant.save()
        participant_answers = \
            [record.answer for record in
             TestParticipantAnswers.objects.filter(test=test, test_participant=test_participant).order_by(
                 'question_id')]
        result = None
        if participant_answers:
            result = sum(1 if a.is_correct else 0 for a in participant_answers)
        return render(request, 'quiz/detail.html',
                      {'test': test, 'questions': questions, 'test_participant': test_participant, 'result': result})


@login_required
def results(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    questions = test.question_set.order_by('id')
    test_participant = TestParticipant.objects.get(test=test, user=request.user)
    participant_answers = \
        [record.answer for record in
         TestParticipantAnswers.objects.filter(test=test, test_participant=test_participant).order_by('question_id')]
    result = [(question.question_text, answer.answer_text, 1 if answer.is_correct else 0)
              for question, answer in zip(questions, participant_answers)]
    points = sum(1 if a.is_correct else 0 for a in participant_answers)
    context = {'test': test, 'result': result, 'points': points}
    return render(request, 'quiz/results.html', context)


@login_required
def answer_the_question(request, test_id, question_id):
    answer = Answer.objects.get(pk=request.POST.get('answer'))
    test = get_object_or_404(Test, pk=test_id)
    participant_id = TestParticipant.objects.get(test=test, user=request.user).id
    try:
        test_participant_answer = TestParticipantAnswers.objects.get(test_participant=participant_id, test=test_id,
                                                                     question=question_id)
        test_participant_answer.answer = answer
    except ObjectDoesNotExist:
        test_participant_answer = TestParticipantAnswers(test_participant=get_object_or_404(TestParticipant, id=participant_id),
                                                         test=test,
                                                         question=get_object_or_404(Question, id=question_id),

                                                         answer=answer)
    finally:
        test_participant_answer.save()
        return HttpResponseRedirect(reverse('quiz:question', args=(test_id, question_id)))
