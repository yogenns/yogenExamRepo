from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=1024, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    QUESTION_TYPES = (
        ('M', 'Multiple Selection'),
        ('S', 'Single Selection')
    )
    question = models.TextField()
    options = models.TextField()  # Store Dict of applicable choices
    answer = models.TextField()  # Store List of applicable choices
    _question_type = models.CharField(max_length=1, choices=QUESTION_TYPES)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    explaination = models.TextField()

    def question_type(self):
        return (dict(self.QUESTION_TYPES))[self._question_type]

    def __str__(self):
        return self.question


class Exam(models.Model):
    name = models.TextField()
    question_count = models.PositiveSmallIntegerField()
    questions = models.ManyToManyField(Question)
    time = models.TimeField()
    passing_percentage = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(1)])

    def __str__(self):
        return self.name


class ExamAttempt(models.Model):
    RESULT_STATUS = (
        ('P', 'PASS'),
        ('F', 'FAIL')
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    answer_list = models.TextField()
    result_attempted_question_count = models.PositiveSmallIntegerField(
        blank=True, null=True)
    result_correct_answer_count = models.PositiveSmallIntegerField(
        blank=True, null=True)
    result_percentage = models.PositiveSmallIntegerField(blank=True, null=True,
                                                         validators=[MaxValueValidator(100), MinValueValidator(0)])
    _result_status = models.CharField(max_length=1, choices=RESULT_STATUS)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    def result_status(self):
        if self._result_status == '':
            return "No Result"
        else:
            return (dict(self.RESULT_STATUS))[self._result_status]
