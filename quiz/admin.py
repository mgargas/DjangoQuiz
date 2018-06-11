from django.contrib import admin

# Register your models here.
from .models import *


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


admin.site.register(Test)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(TestParticipant)
admin.site.register(TestParticipantAnswers)
