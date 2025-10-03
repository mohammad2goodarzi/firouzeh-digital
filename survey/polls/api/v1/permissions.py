from rest_framework.permissions import BasePermission

from polls.models import Participation


class IsSurveyParticipant(BasePermission):
    def has_permission(self, request, view):
        survey_id = view.kwargs.get('pk')
        user_id = request.profile.user_id

        if not user_id or not survey_id:
            return False

        return Participation.objects.filter(
            survey_id=survey_id,
            user_id=user_id
        ).exists()
