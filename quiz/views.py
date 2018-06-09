from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import *


class IndexView(generic.ListView):
    template_name = 'quiz/index.html'
    context_object_name = 'latest_test_list'

    def get_queryset(self):
        """"Return the last five tests"""
        return Test.objects.all()[:4]


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


def answer_the_question(request, test_id, question_id):
    ide = int(request.POST['answer'])
    answer = get_object_or_404(Answer, id=ide)
    test_participant_answer = get_object_or_404(TestParticipantAnswers, test_participant=1, test=test_id,
                                                question=question_id)
    test_participant_answer.answer = answer
    test_participant_answer.save()
    return HttpResponseRedirect(reverse('quiz:detail', args=(test_id,)))

