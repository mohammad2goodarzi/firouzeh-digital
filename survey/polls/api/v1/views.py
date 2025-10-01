from rest_framework.generics import ListAPIView, RetrieveAPIView

from polls.api.v1.serializers import SurveySerializer, SurveyDetailSerializer
from polls.models import Survey


class SurveyListAPIView(ListAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


class SurveyRetrieveAPIView(RetrieveAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveyDetailSerializer
