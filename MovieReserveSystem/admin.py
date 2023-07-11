from django.contrib import admin

# Register your models here.
from MovieReserveSystem.models import Movies, Schedule, Reservations
admin.site.register(Movies)
admin.site.register(Schedule)
admin.site.register(Reservations)
