from django.urls import path
from . import views
from  .views import register_user

urlpatterns = [
    # path("", views.index, name="index"),
    path('api/register/', register_user, name='register'),
    
]
