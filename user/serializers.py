from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password','confirm_password']
        # fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

class UserSignupSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=100, style={'input_type': 'password', 'placeholder': 'Confirm Password'})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError("A user is already registered with this email, sign in instead")

        if data.get('role') not in dict(User.ROLE_CHOICES):
            raise serializers.ValidationError("Invalid role")

        return data

    def create(self, validated_data):
        del validated_data['confirm_password']
        user = User.objects.create_user(**validated_data)
        return user

class UserSigninSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, style={'placeholder': 'Email', 'autofocus': True})
    password = serializers.CharField(max_length=100, style={'input_type': 'password', 'placeholder': 'Password'})