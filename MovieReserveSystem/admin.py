from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.
from .models import Movie, Schedule, Reservation, Hole, Seat

from django.contrib.auth import get_user_model


admin.site.register(Movie)
admin.site.register(Schedule)
admin.site.register(Reservation)
admin.site.register(Hole)
admin.site.register(Seat)

CustomUser = get_user_model()
admin.site.register(CustomUser)  # Userモデルを登録
admin.site.unregister(Group)  # Groupモデルは不要のため非表示にします
