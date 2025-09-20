from django.db import models

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    # image = models.ImageField(upload_to='event_images/', blank=True, null=True)

    def __str__(self):
        return self.title