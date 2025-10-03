from django.db import models


class Survey(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    valid_since = models.DateTimeField()
    valid_until = models.DateTimeField()


class Question(models.Model):
    survey = models.ForeignKey(to=Survey, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    required = models.BooleanField(default=True)


class Choice(models.Model):
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)


class Participation(models.Model):
    survey = models.ForeignKey(to=Survey, on_delete=models.CASCADE)
    user_id = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['survey', 'user_id'], name='unique_participation_per_user')
        ]


class Answer(models.Model):
    participation = models.ForeignKey(to=Participation, on_delete=models.CASCADE)
    choice = models.ForeignKey(to=Choice, on_delete=models.CASCADE)
