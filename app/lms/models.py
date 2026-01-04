from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("dosen", "Dosen"),
        ("mahasiswa", "Mahasiswa"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="mahasiswa")

    def __str__(self):
        return f"{self.username} ({self.role})"


class Course(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    instructor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="courses_taught"
    )

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Assignment(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="assignments"
    )
    title = models.CharField(max_length=200)
    deadline = models.DateTimeField()

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name="submissions"
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    answer = models.TextField()
    grade = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} -> {self.assignment.title}"
