from django.contrib import admin
from e_absen_backend.models.model_user import User_Id
from e_absen_backend.models.model_role import Role
from e_absen_backend.models.model_shift_time import Shift

@admin.register(User_Id)
class UserIdAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_name', 'user_avatar', 'user_role', 'user_location', 'user_payout', 'user_shift', 'is_active')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_id', 'role_name', 'is_active')

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('shift_id', 'shift_name', 'shift_time_in', 'shift_time_out', 'is_active')