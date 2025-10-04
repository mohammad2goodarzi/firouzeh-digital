from datetime import datetime

import pytest
from django.utils import timezone

from polls.models import Survey, Question, Choice


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def access_token():
    return 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwidXNlcl9pZCI6MTAwMCwiaWF0IjoxNTE2MjM5MDIyfQ.YRd5yoyFYNVcX2up5d3uN0U-KP3Bi_Lhpv9JVDyxcQA'


@pytest.fixture
def valid_survey():
    tz = timezone.get_current_timezone()
    survey = Survey.objects.create(
        title='title1',
        description='description1',
        valid_since=datetime(2025, 1, 1, 9, 0, 0, tzinfo=tz),
        valid_until=datetime(2026, 1, 3, 9, 0, 0, tzinfo=tz),
    )
    q1 = Question.objects.create(
        survey=survey,
        text='question1 text',
        required=True,
    )
    Choice.objects.create(
        question=q1,
        text='question1 choice1',
    )
    Choice.objects.create(
        question=q1,
        text='question1 choice2',
    )
    q2 = Question.objects.create(
        survey=survey,
        text='question2 text',
        required=True,
    )
    Choice.objects.create(
        question=q2,
        text='question2 choice1',
    )
    Choice.objects.create(
        question=q2,
        text='question2 choice2',
    )
    return survey


@pytest.fixture
def invalid_survey():
    tz = timezone.get_current_timezone()
    survey = Survey.objects.create(
        title='title1',
        description='description1',
        valid_since=datetime(2024, 1, 1, 9, 0, 0, tzinfo=tz),
        valid_until=datetime(2024, 1, 3, 9, 0, 0, tzinfo=tz),
    )
    q1 = Question.objects.create(
        survey=survey,
        text='question1 text',
        required=True,
    )
    Choice.objects.create(
        question=q1,
        text='question1 choice1',
    )
    Choice.objects.create(
        question=q1,
        text='question1 choice2',
    )
    return survey
