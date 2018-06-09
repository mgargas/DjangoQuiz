from django.urls import path

from . import views
app_name = 'quiz'
urlpatterns = [
    # ex: /quiz/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /quiz/5/
    path('<int:test_id>/', views.detail, name='detail'),
    # ex: /quiz/5/results/
    path('<int:test_id>/<int:question_id>/answer_the_question/', views.answer_the_question, name='answer_the_question'),
    path('<int:test_id>/results/', views.results, name='results'),

]
