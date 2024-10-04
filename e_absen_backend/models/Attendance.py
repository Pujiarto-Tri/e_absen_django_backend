from django.db import models
from e_absen_backend.models.Employee import Employee
from datetime import time, date
from e_absen_backend.models.Shift import Shift  # Import the Shift model

class Attendance(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True)  # Reference to the Shift model
    attendance_date = models.DateField(auto_now_add=True)
    check_in_time = models.TimeField(null=True, blank=True)  # Actual check-in time
    check_out_time = models.TimeField(null=True, blank=True)  # Actual check-out time
    is_late = models.BooleanField(default=False)
    left_early = models.BooleanField(default=False)
    is_weekend = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Attendances"
        verbose_name = "Attendance"
        unique_together = ('user', 'attendance_date')  # Ensure only one record per user per date

    def save(self, *args, **kwargs):
        # Check if the attendance date falls on a weekend (Saturday or Sunday)
        if self.attendance_date.weekday() in [5, 6]:  # 5 = Saturday, 6 = Sunday
            self.is_weekend = True
        
        # Check if the user checked in late
        if self.check_in_time and self.shift and self.check_in_time > self.shift.shift_time_in:
            self.is_late = True
        else:
            self.is_late = False

        # Check if the user left early
        if self.check_out_time and self.shift and self.check_out_time < self.shift.shift_time_out:
            self.left_early = True
        else:
            self.left_early = False

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.name} - {self.attendance_date} - {self.shift.shift_name}'

