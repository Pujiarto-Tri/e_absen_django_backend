from django.contrib import admin
from e_absen_backend.models.Employee import Employee
from e_absen_backend.models.Role import Role
from e_absen_backend.models.Shift import Shift
from e_absen_backend.models.Location import Location
from e_absen_backend.models.Attendance import Attendance

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'employee_name', 'user_avatar', 'user_role', 'user_location', 'user_payout', 'user_shift', 'is_active')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_id', 'role_name', 'is_active')

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('shift_id', 'shift_name', 'shift_time_in', 'shift_time_out', 'is_active')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_id', 'location_name', 'location_spot', 'location_radius', 'is_active')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'shift', 'attendance_date', 'check_in_time', 'check_out_time', 'is_late', 'left_early', 'is_weekend')