"""
URL configuration for e_absen_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenRefreshView

from e_absen_backend.views import UserRegistrationView, EmployeeProfileView, login_view, CheckInView, CheckOutView, EmployeeAttendanceForCurrentMonthView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('e_absen_backend/', include("e_absen_backend.urls")),
    path('api/register/', UserRegistrationView.as_view(), name='user_registration'),
    path('api/login/', login_view, name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/employee/profile/', EmployeeProfileView.as_view(), name='employee-profile'),
    path('attendance/checkin/', CheckInView.as_view(), name='check-in'),
    path('attendance/checkout/', CheckOutView.as_view(), name='check-out'),
    path('attendance/mine/', EmployeeAttendanceForCurrentMonthView.as_view(), name='employee-attendance-current-month'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)