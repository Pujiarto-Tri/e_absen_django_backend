from django.urls import path
from . import views
from  .views import UserRegistrationView

urlpatterns = [
    # path("", views.index, name="index"),
    path('api/register/', UserRegistrationView.as_view(), name='user_registration'),
    
]
