from django.db import models
from django.contrib.auth.models import User
from .model_role import Role
from .model_shift_time import Shift
from .model_location import Location

class User_Id(models.Model):
    class Meta:
        verbose_name_plural = 'Users'
        verbose_name = 'User'
    
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    user_avatar = models.ImageField(blank=True, null=True, upload_to="avatar")
    user_name = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    user_role = models.ForeignKey(Role, on_delete=models.CASCADE)
    user_payout = models.CharField(max_length=500, null=True)
    user_shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    user_location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_name}'
