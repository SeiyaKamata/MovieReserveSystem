from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

import uuid

class CustomUser(AbstractUser):
    pass

# Create your models here.
class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, help_text='映画名')
    poster = models.ImageField(upload_to='images')
    screen_time = models.IntegerField(default=90, help_text='上映時間')
    is_deleted = models.BooleanField(default=False, help_text='削除されたらTrue')

    def __str__(self):
        return self.name

class Hole(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, help_text='ホール名')
    row = models.IntegerField(default=0, help_text='行')
    col = models.IntegerField(default=0, help_text='列')

    def __str__(self):
        return f"{self.name}"

class Seat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hole = models.ForeignKey(Hole, on_delete=models.CASCADE)
    row = models.IntegerField(default=0, help_text='行')
    col = models.IntegerField(default=0, help_text='列')

    def __str__(self):
        return f"{chr(self.row+64)}-{self.col}"


class Schedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    hole = models.ForeignKey(Hole, on_delete=models.CASCADE)
    start_at = models.DateTimeField(null=True, help_text='上映日時')
    is_deleted = models.BooleanField(default=False, help_text='削除されたらTrue')
    is_sold_out = models.BooleanField(default=False, help_text='満席ならTrue')

    def __str__(self):
        return f"{self.movie} on {self.start_at}"


class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, null=True, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False, help_text='削除されたらTrue')
    created_at = models.DateTimeField(default=timezone.now, help_text='作成日')

    def __str__(self):
        return f"{self.seat}"