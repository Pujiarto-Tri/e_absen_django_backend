from django.urls import path
from .views import UserRegistrationView
from .views import login_view
from .views import EmployeeProfileView

urlpatterns = [
    # path("", views.index, name="index"),
    path('api/register/', UserRegistrationView.as_view(), name='user_registration'),
    path('login/', login_view, name='login'),
    path('api/employee/profile/', EmployeeProfileView.as_view(), name='employee-profile'),
]
