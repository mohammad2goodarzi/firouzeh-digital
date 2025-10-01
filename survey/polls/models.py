from django.db import models


QUESTION_TYPES = [
    ('single', 'single'),
    ('multiple', 'multiple'),
]


class Logged(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created_at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated_at')


class Survey(Logged):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)


class Question(Logged):
    survey = models.ForeignKey(to=Survey, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default='single')
    required = models.BooleanField(default=True)


class Choice(Logged):
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
