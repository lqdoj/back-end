from submissions.models import Submission
from django.contrib import admin


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('task', 'user')


admin.site.register(Submission, SubmissionAdmin)
