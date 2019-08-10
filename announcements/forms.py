from django.forms import ModelForm
from .models import Announcement


class AnnouncementForm(ModelForm):
    class Meta:
        model = Announcement
        fields = {"title", "author", "content", "time", "last_edited"}