from django.db.models import Count, Prefetch
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

from polls.api.v1.serializers import SurveySerializer, SurveyDetailSerializer, ParticipationSerializer, ResultSerializer
from polls.models import Survey, Choice, Question


class SurveyListAPIView(ListAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


class SurveyRetrieveAPIView(RetrieveAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveyDetailSerializer


class ParticipationCreateAPIView(CreateAPIView):
    serializer_class = ParticipationSerializer


class ResultAPIView(ListAPIView):
    serializer_class = ResultSerializer

    def get_queryset(self):
        survey_id = self.kwargs['pk']
        questions_with_choices = Question.objects.filter(
            survey_id=survey_id
        ).prefetch_related(
            Prefetch(
                'choice_set',
                queryset=Choice.objects.annotate(vote_count=Count('answer'))
            )
        )
        return questions_with_choices
