from django.contrib import admin
from rota.models import UserProfile, Request, Timetable

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Request)
admin.site.register(Timetable)
