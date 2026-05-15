from django.db import models

from django.contrib.auth.models import User


class Teacher(models.Model):

    user = models.OneToOneField(

        User,

        on_delete=models.CASCADE

    )

    phone = models.CharField(
        max_length=15
    )

    subject = models.CharField(
        max_length=100
    )

    role = models.CharField(
        max_length=50,
        default='Teacher'
    )

    def __str__(self):

        return self.user.first_name