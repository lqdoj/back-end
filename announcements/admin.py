from django.contrib import admin
from .models import Announcement


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'time', 'last_edited')


admin.site.register(Announcement, AnnouncementAdmin)
