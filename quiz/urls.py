from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
app_name = 'quiz'
urlpatterns = [
    # ex: /quiz/
    path('', views.index, name='index'),
    # ex: /quiz/5/
    path('<int:test_id>/<int:question_id>/answer_the_question/', views.answer_the_question, name='answer_the_question'),
    path('<int:test_id>/<int:question_id>/', views.question, name='question'),
    path('<int:test_id>/', views.detail, name='detail'),
    # ex: /quiz/5/results/
    path('<int:test_id>/results/', views.results, name='results'),
    path('leaderboard', views.leaderboard, name='leaderboard'),
]


