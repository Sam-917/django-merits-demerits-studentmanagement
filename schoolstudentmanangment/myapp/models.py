
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.contrib.auth.models import User

class Grade(models.Model):
    form_number = models.CharField(max_length=10)

    def __str__(self):
        return f"Form {self.form_number}"

class Class(models.Model):

    grade = models.ForeignKey(Grade, related_name='classes', on_delete=models.CASCADE)
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    
class MeritStudent(models.Model):
    student_name = models.CharField(max_length=255)
    teacher_responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.TextField()
    ic_number = models.CharField(max_length=20)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)  
    upload_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student_name} - Merit"

class DemeritStudent(models.Model):
    student_name = models.CharField(max_length=255)
    teacher_responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.TextField()
    ic_number = models.CharField(max_length=20)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    upload_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student_name} - Demerit"

