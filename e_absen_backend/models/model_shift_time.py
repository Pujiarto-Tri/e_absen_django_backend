from django.db import models

class Shift(models.Model):
    class Meta:
        verbose_name_plural = 'Shifts'
        verbose_name = 'Shift'
    
    shift_id = models.AutoField(primary_key=True)
    shift_name = models.CharField(max_length=200, blank=True)
    shift_time_in = models.TimeField(null=True)
    shift_time_out = models.TimeField(null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.shift_name}'
    
    