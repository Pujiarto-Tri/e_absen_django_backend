from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    class Meta:
        verbose_name_plural = 'Roles'
        verbose_name = 'Role'
    
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.role_name}'