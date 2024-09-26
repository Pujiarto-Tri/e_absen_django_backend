from django.urls import path
from . import views
from  .views import UserRegistrationView

urlpatterns = [
    # path("", views.index, name="index"),
    path('api/register/', UserRegistrationView, name='register'),
    
]
