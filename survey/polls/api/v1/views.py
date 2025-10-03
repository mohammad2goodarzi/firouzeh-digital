from django.db.models import Count, Prefetch
from django.utils import timezone
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

from polls.api.v1.permissions import IsSurveyParticipant
from polls.api.v1.serializers import SurveySerializer, SurveyDetailSerializer, ParticipationSerializer, ResultSerializer
from polls.models import Survey, Choice, Question


class SurveyListAPIView(ListAPIView):
    queryset = Survey.objects.valid()
    serializer_class = SurveySerializer


class SurveyRetrieveAPIView(RetrieveAPIView):
    queryset = Survey.objects.valid()
    serializer_class = SurveyDetailSerializer


class ParticipationCreateAPIView(CreateAPIView):
    serializer_class = ParticipationSerializer


class ResultAPIView(ListAPIView):
    serializer_class = ResultSerializer
    permission_classes = [IsSurveyParticipant]

    def get_queryset(self):
        now = timezone.now()
        survey_id = self.kwargs['pk']
        questions_with_choices = Question.objects.filter(
            survey_id=survey_id,
            survey_id__valid_since__lte=now,
            survey_id__valid_until__gt=now,
        ).prefetch_related(
            Prefetch(
                'choice_set',
                queryset=Choice.objects.annotate(vote_count=Count('answer'))
            )
        )
        return questions_with_choices
