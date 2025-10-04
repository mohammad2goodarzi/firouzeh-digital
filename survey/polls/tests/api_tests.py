import pytest
from django.urls import reverse_lazy
from django.utils import timezone
from freezegun import freeze_time

from polls.models import Survey, Participation

view_url_parameters = [
    ('v1:survey-list', {}, '/polls/api/v1/surveys'),
    ('v1:survey-detail', {'pk': 1}, '/polls/api/v1/surveys/1'),
    ('v1:user-participation', {}, '/polls/api/v1/participation'),
    ('v1:survey-result', {'pk': 1}, '/polls/api/v1/surveys/1/result'),
]


@pytest.mark.parametrize(
    'view_name, view_reverse_kwargs, view_url',
    view_url_parameters
)
@pytest.mark.django_db
def test_view_url(view_name, view_reverse_kwargs, view_url):
    url = reverse_lazy(view_name, kwargs=view_reverse_kwargs)
    # you should be aware that this url should not change
    assert url == view_url


@pytest.mark.django_db
@freeze_time("2025-01-02")  # why this is not working inside the api?
def test_survey_list_response(api_client, access_token, valid_survey, invalid_survey):
    url = reverse_lazy('v1:survey-list')
    response = api_client.get(path=url, HTTP_AUTHORIZATION=access_token)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert Survey.objects.all().count() == 2


@pytest.mark.django_db
@freeze_time("2025-01-02")  # why this is not working inside the api?
def test_survey_detail_response(api_client, access_token, valid_survey, invalid_survey):
    url = reverse_lazy('v1:survey-detail', kwargs={'pk': valid_survey.pk})
    response = api_client.get(path=url, HTTP_AUTHORIZATION=access_token)
    assert response.status_code == 200
    assert len(response.json()['question_set']) == 2
    assert len(response.json()['question_set'][0]['choice_set']) == 2
    assert len(response.json()['question_set'][1]['choice_set']) == 2


@pytest.mark.django_db
@freeze_time("2025-01-02")  # why this is not working inside the api?
def test_invalid_survey_detail_response(api_client, access_token, valid_survey, invalid_survey):
    url = reverse_lazy('v1:survey-detail', kwargs={'pk': invalid_survey.pk})
    response = api_client.get(path=url, HTTP_AUTHORIZATION=access_token)
    assert response.status_code == 404


@pytest.mark.django_db
@freeze_time("2025-01-02")  # why this is not working inside the api?
def test_survey_participation_response(api_client, access_token, valid_survey, invalid_survey):
    participation_count1 = Participation.objects.count()
    user_id = 100
    questions = valid_survey.question_set.all()
    choices = [q.choice_set.all().first() for q in questions]
    data = {
        "survey": valid_survey.pk,
        "user_id": user_id,
        "answers": [
            {
                "choice": ch.pk
            } for ch in choices
        ]
    }
    url = reverse_lazy('v1:user-participation')
    response = api_client.post(path=url, HTTP_AUTHORIZATION=access_token, data=data, format='json')
    assert response.status_code == 201
    assert Participation.objects.count() == participation_count1 + 1


@pytest.mark.django_db
@freeze_time("2025-01-02")  # why this is not working inside the api?
def test_invalid_survey_participation_response(api_client, access_token, valid_survey, invalid_survey):
    participation_count1 = Participation.objects.count()
    user_id = 100
    questions = invalid_survey.question_set.all()
    choices = [q.choice_set.all().first() for q in questions]
    data = {
        "survey": invalid_survey.pk,
        "user_id": user_id,
        "answers": [
            {
                "choice": ch.pk
            } for ch in choices
        ]
    }
    url = reverse_lazy('v1:user-participation')
    response = api_client.post(path=url, HTTP_AUTHORIZATION=access_token, data=data, format='json')
    assert response.status_code == 400
    assert Participation.objects.count() == participation_count1


@pytest.mark.django_db
@freeze_time("2025-01-02")  # why this is not working inside the api?
def test_survey_result_response(api_client, access_token, valid_survey, invalid_survey):
    url = reverse_lazy('v1:survey-result', kwargs={'pk': valid_survey.pk})
    response = api_client.get(path=url, HTTP_AUTHORIZATION=access_token)
    assert response.status_code == 403

    questions = valid_survey.question_set.all()
    choices = [q.choice_set.all().first() for q in questions]
    data = {
        "survey": valid_survey.pk,
        "answers": [
            {
                "choice": ch.pk
            } for ch in choices
        ]
    }
    url2 = reverse_lazy('v1:user-participation')
    api_client.post(path=url2, HTTP_AUTHORIZATION=access_token, data=data, format='json')
    response = api_client.get(path=url, HTTP_AUTHORIZATION=access_token)
    assert response.status_code == 200
