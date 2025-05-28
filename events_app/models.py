from django.db import models
from django.conf import settings

class Events(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    date = models.DateField()
    location = models.CharField(max_length=100)
    organaizer = models.CharField(max_length=100)

    attendees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='registered_events',
        blank=True
    )

    def __str__(self):
        return self.title