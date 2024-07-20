from django.urls import path
from .views import UserSignupPortal, UserSigninPortal

urlpatterns = [
    path('register/', UserSignupPortal.as_view(), name='register'),
    path('login/', UserSigninPortal.as_view(), name='login'),
]