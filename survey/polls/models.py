from django.db import models
from django.utils import timezone


class SurveyQuerySet(models.QuerySet):
    def valid(self, *args, **kwargs):
        now = timezone.now()
        return super(SurveyQuerySet, self).filter(*args, **kwargs).filter(
            valid_since__lte=now,
            valid_until__gt=now,
        )


class Survey(models.Model):
    objects = SurveyQuerySet.as_manager()

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    valid_since = models.DateTimeField()
    valid_until = models.DateTimeField()

    @property
    def is_valid(self):
        now = timezone.now()
        return self.valid_since <= now < self.valid_until


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
