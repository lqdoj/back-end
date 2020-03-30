from rest_framework import serializers
from submissions.models import Submission
from tasks.models import Task


class SubmissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('id', 'task', 'language', 'result', 'submit_time')


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
