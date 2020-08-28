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

    # def set_answer(self, x):
    #    self.answer = json.dumps(x)

    # def get_answer(self):
    #    return json.loads(self.answer)

    # def set_options(self, x):
    #    self.options = json.dumps(x)

    # def get_options(self):
    #    return json.loads(self.options)

    def question_type(self):
        return (dict(self.QUESTION_TYPES))[self._question_type]
