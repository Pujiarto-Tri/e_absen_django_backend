from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    class Meta:
        verbose_name_plural = 'Locations'
        verbose_name = 'Location'
    
    location_id = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.location_name}'