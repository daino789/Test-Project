from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.authtoken.models import Token


class SignupSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(label=("Email"))
    username = serializers.CharField(label=("Username"))
    password = serializers.CharField(label=("Password"), style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate(self, attrs):
        email = attrs.get('email')  
        username = attrs.get('username')
        password = attrs.get('password')
        if email and password:
            is_exists = User.objects.filter(email= email).exists()

            if not is_exists:
                user = User.objects.filter(username= username).exists()

                if user:
                    msg = "Please enter a unique username"
                    raise serializers.ValidationError(msg, code='authorization')

            else: 
                msg = "Email already exist"
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = "Please enter Email and Password"
            raise serializers.ValidationError(msg, code='authorization')

        return attrs
 

class LoginSerializer(serializers.Serializer):
    """
    Authentication serializer. 
    Here, Valid method check if not valid user raise exception or if authenticate return user instance.
    """
    email = serializers.EmailField(label=("Email"))
    password = serializers.CharField(label=("Password"), style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user_obj = User.objects.filter(email= email)

            if user_obj:
                user = authenticate(username=user_obj[0].username, password=password)  

                if user:
                    if not user.is_active:
                        msg = ({'user': 'User account is disabled.'})
                        raise serializers.ValidationError(msg, code='authorization')

                else:
                    msg = ({'login' : 'Unable to log in with provided credentials.'})
                    raise serializers.ValidationError(msg, code='authorization')

            else:
                msg = ({'email' : 'email address is not correct or user is not valid user type.'})
                raise serializers.ValidationError(msg, code='authorization')

        else:
            if not email and not password:
                msg = ({
                  'email': 'Must include "email"',
                  'password': 'Must include "password".'
                  })
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class LogoutSerializer(serializers.Serializer):

    token = serializers.CharField(label=("Token"))

    def validate(self, attrs):
        token = attrs.get('token')
        if token:
            tokenobj = Token.objects.filter(key=token)

            if not tokenobj:
                msg = ({'token' : 'Invalid token.'})
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = ({'token' : 'Must include "token".'})
            raise serializers.ValidationError(msg, code='authorization')

        attrs['token'] = tokenobj
        return attrs
    
