from django.db import models
from django.contrib.auth.models import User
from .Role import Role
from .Shift import Shift
from .Location import Location

class Employee(models.Model):
    class Meta:
        verbose_name_plural = 'Employees'
        verbose_name = 'Employe'
    
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    user_avatar = models.ImageField(blank=True, null=True, upload_to="avatar")
    employee_name = models.CharField(max_length=200, blank=True, null=True)  # Changed from user_name to name
    is_active = models.BooleanField(default=True)
    user_role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    user_payout = models.CharField(max_length=500, null=True, blank=True)
    user_shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True)
    user_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.employee_name or self.user_id.email}'