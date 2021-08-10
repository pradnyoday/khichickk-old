from .models import Users,Profile
from rest_framework import serializers
from rest_framework.response import Response

from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = Users
        fields = ('id', 'email', 'first_name', 'last_name', 'password')
        

class UsersSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'email')

class ProfileSerializer(serializers.ModelSerializer):
    user_first_name = serializers.CharField(source='user.first_name')
    user_last_name = serializers.CharField(source='user.last_name')
    user_email = serializers.CharField(source='user.email')    
    class Meta:
        model = Profile
        fields = ('user_first_name', 'user_last_name', 'user_email','image','bio','gender','experience','num_following','num_followers','followers','following','city','state','country','phone')
        