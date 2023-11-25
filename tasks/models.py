import uuid
from django.db import models
from django.contrib.auth.models import User


class ToDo(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_as_leader', blank=True, null=True)
    add_mark = models.CharField(blank=False, null=False, max_length=255)
    is_deleted = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    subject = models.ForeignKey("tasks.Subject", blank=True, null=False, on_delete=models.CASCADE)
    date = models.DateField()
    exam = models.ForeignKey("tasks.Exam", on_delete=models.CASCADE)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        verbose_name_plural = "ToDo"

    def __str__(self):
        return self.add_mark
    

class Subject(models.Model):
    name = models.CharField(max_length=225)
    class Meta:
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.name
    
    


class Exam(models.Model):
    name = models.CharField(max_length=225)

    class Meta:
        verbose_name_plural = "Exams"

    def __str__(self):
        return self.name