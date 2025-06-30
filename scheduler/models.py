from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
class Provider(models.Model):
    name = models.CharField(max_length=255)


class Availability(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='availabilities')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time")


class Appointment(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='appointments')
    client_name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time")

    class Meta:
        indexes = [
            models.Index(fields=['provider', 'start_time']),
        ]