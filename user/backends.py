from django.contrib.auth.backends import ModelBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions
from rest_framework.response import Response
from .models import User
from django.conf import settings
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken


def enforce_csrf(request):
    check = CSRFCheck()
    check.process_request(request)
    reason = check.process_view(request, None, (), {})
    if reason:
        raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)

class UserBackend(ModelBackend):
    def authenticate(self, request, email=None,password=None):
        email = ['email']
        password = ['password']
        try:
            user = User.objects.get(email=email)
            if user.check_password(password) is True:
                return user
        except User.DoesNotExist:
            pass      
        return None    

class UpdatedJWTAuthentication(JWTAuthentication):
    #Either from header or from cookie
    def authenticate(self, request):
        header = self.get_header(request)
        
        if header is None:
            #If not present in header check in cookie passed.
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None
            # print(raw_token)
        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None
        
        validated_token = self.get_validated_token(raw_token)

      
        return self.get_user(validated_token), validated_token
