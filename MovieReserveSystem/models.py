from django.db import models
# from djnago.contrib.auth.models import AbstractBaseUser
import uuid
from django.contrib.auth import get_user_model


# Create your models here.
class Movies(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, help_text='映画名')

    def __str__(self):
        return self.name


class Schedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    data_and_time = models.DateTimeField(help_text='上映日時')

    def __str__(self):
        return f"{self.movie} on {self.data_and_time}"

# class Users(AbstractBaseUser):


class Reservations(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return "test"