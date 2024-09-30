from django.urls import path
from .views import UserRegistrationView
from .views import login_view

urlpatterns = [
    # path("", views.index, name="index"),
    path('api/register/', UserRegistrationView.as_view(), name='user_registration'),
    path('login/', login_view, name='login'),
    
]
