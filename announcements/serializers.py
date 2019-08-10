from .models import Announcement
from rest_framework import serializers


class AnnouncementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Announcement
        fields = '__all__'
    # title = serializers.CharField(max_length=200)
    # author = serializers.CharField()
    # content = serializers.CharField()
    # time = serializers.DateTimeField()
    # last_edited = serializers.DateTimeField()
