from django.db import models


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
    required = models.BooleanField(default=True)


class Choice(Logged):
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)


class Participation(models.Model):
    survey = models.ForeignKey(to=Survey, on_delete=models.CASCADE)
    user_id = models.IntegerField()


class Answer(models.Model):
    participation = models.ForeignKey(to=Participation, on_delete=models.CASCADE)
    choice = models.ForeignKey(to=Choice, on_delete=models.CASCADE)
