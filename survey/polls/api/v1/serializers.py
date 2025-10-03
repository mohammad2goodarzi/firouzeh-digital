from rest_framework import serializers

from polls.models import Survey, Question, Choice, Answer, Participation


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    choice_set = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'


class SurveyDetailSerializer(serializers.ModelSerializer):
    question_set = QuestionSerializer(many=True)

    class Meta:
        model = Survey
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        exclude = ['participation']


class ParticipationSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, write_only=True)

    class Meta:
        model = Participation
        fields = '__all__'

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        participation = Participation.objects.create(**validated_data)
        Answer.objects.bulk_create([
            Answer(participation=participation, **answer_data)
            for answer_data in answers_data
        ])
        return participation
