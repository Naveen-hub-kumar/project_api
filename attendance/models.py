from django.db import models
from students.models import Student

class Attendance(models.Model):

    STATUS_CHOICES = (

        ('Present', 'Present'),

        ('Absent', 'Absent'),

    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )

    class Meta:

        unique_together = ['student', 'date']

    def __str__(self):

        return f"{self.student.name} - {self.date}"