from django.urls import path, include

from . import views

app_name = 'polls'


urlpatterns = [
    path('surveys', views.SurveyListAPIView.as_view(), name="survey-list"),
    path('surveys/<int:pk>', views.SurveyRetrieveAPIView.as_view(), name="survey-detail"),
]
