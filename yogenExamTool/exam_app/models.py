from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

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
