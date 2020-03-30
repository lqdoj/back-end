from enum import Enum
from django.db import models
from tasks.models import Task
from users.models import User


class Language(Enum):
    JAVA = "Java"
    CPP = "C++"
    PYTHON = "Python"


class Submission(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field="username")
    source_code = models.TextField()
    submit_time = models.DateTimeField(auto_now=True)
    language = models.CharField(max_length=20, choices=[(language.name, language.value) for language in Language])
    result = models.CharField(max_length=100, default="", blank=True)
