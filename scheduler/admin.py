from django.contrib import admin
from .models import Provider, Availability, Appointment

admin.site.register(Provider)
admin.site.register(Availability)
admin.site.register(Appointment)
# Register your models here.
