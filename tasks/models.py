from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    tag_name = models.CharField(max_length=50, unique=True, primary_key=True)

    def __str__(self):
        return self.tag_name


class Task(models.Model):
    task_code = models.CharField(max_length=8, unique=True, primary_key=True)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, to_field="username")
    description = models.TextField()
    tags = models.ManyToManyField(Tag)
    score_mode = models.CharField(max_length=10)
    score_parameter = models.IntegerField(default=None)
    time_limit = models.FloatField(default=1)
    memory_limit = models.IntegerField(default=256)
    diff_mode = models.CharField(max_length=10)
    custom_grader = models.CharField(default=None, max_length=100)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_code + " by " + self.author.__str__()


class Test(models.Model):
    id = models.IntegerField(primary_key=True)
    task = models.ForeignKey(Task, to_field="task_code", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    position = models.IntegerField()
    input = models.FileField()
    output = models.FileField()
