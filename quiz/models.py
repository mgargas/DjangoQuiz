from django.db import models

# Create your models here.


class Test(models.Model):
    test_name = models.CharField(max_length=200)

    def __str__(self):
        return self.test_name


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text


class TestParticipant(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    participant_name = models.CharField(max_length=200)
    participant_surname = models.CharField(max_length=200)

    def __str__(self):
        return self.participant_name + self.participant_surname


class TestParticipantAnswers(models.Model):
    test_participant = models.ForeignKey(TestParticipant, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return self.test_participant.__str__() + self.test_participant.__str__() \
               + self.question.__str__() + self.answer.__str__()

