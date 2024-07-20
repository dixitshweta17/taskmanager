from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model, authenticate,login
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from user.serializers import UserSigninSerializer, UserSignupSerializer
from rest_framework.response import Response
from django.conf import settings

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

#Signup 
class UserSignupPortal(APIView):
    """
    User Signup

    * This view is open to all with password protection.
    * Only registered users are able to access further.
    """
    permission_classes = [permissions.AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'register.html'

    def get(self, request):
        """
        Return user signup portal.
        """
        serializer = UserSignupSerializer()
        return Response({'serializer': serializer})
    
    def post(self, request):
        """
        Parse form on post route
        """
        serializer = UserSignupSerializer(data=request.data)
        
        if not serializer.is_valid():
            print(serializer.errors)
            return Response({'serializer': serializer, 'error': serializer.errors}, template_name='register.html')
        
        # Otherwise save user to database
        user = serializer.save()
        print(user)
        
        # Create a new serializer for the login page
        login_serializer = UserSigninSerializer()

        return Response({'serializer': login_serializer, 'message': 'Registration successful! Please login.'}, template_name='login.html', status=status.HTTP_200_OK)

  
#Signin Portal
class UserSigninPortal(APIView):
    """
    User Signin

    * This view is open to all with password protection.
    """
    permission_classes = [permissions.AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login.html'

    def get(self, request):
        """
        Return user signin portal.
        """
        serializer = UserSigninSerializer()
        print("get serializer", serializer)
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = UserSigninSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'error': serializer.errors})

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(email=email, password=password)

        if user is None:
            return Response({'serializer': serializer, 'error': 'No such user found or incorrect password'})

        print(f"Authenticated user: {user.email}")

        # Log the user in
        login(request, user)
        print(f"Session user: {request.user.email}")

        token_pair = get_tokens_for_user(user)
        
        response = redirect('task-list-create')
        
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=token_pair["access"],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        )
        response.set_cookie(
            key='refresh',
            value=token_pair["refresh"],
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        )
        return response

