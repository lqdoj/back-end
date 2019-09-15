from rest_framework import serializers

from tasks.models import Task


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'task_code', 'title', 'author', 'tags', 'score_mode', 'last_modified')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'task_code', 'title', 'author', 'tags', 'description', 'score_mode', 'last_modified')
