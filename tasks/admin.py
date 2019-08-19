from django.contrib import admin

# Register your models here.
from tasks.models import Task, Tag, Test


class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_code', 'title', 'author')


class TestAdmin(admin.ModelAdmin):
    list_display = ('task', 'name', 'position', 'input', 'output')


admin.site.register(Task, TaskAdmin)
admin.site.register(Tag)
admin.site.register(Test)
