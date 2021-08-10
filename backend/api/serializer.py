from accounts.models import Users,Profile
from rest_framework import serializers
from rest_framework.response import Response

from posts.models import Posts,Ratings
from rest_framework import serializers

from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = Users
        fields = ('id', 'email', 'name', 'password')
        

class UsersSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        fields = ('id','name','email')

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name')
    user_email = serializers.CharField(source='user.email')    
    class Meta:
        model = Profile
        fields = ('user','user_email','image','bio','gender','experience','num_following','num_followers','followers','following','city','state','country','phone')
        
        
class PostsSerializer(serializers.ModelSerializer):
    photographer_name = serializers.CharField(source='photographer.name')
    photographer_email = serializers.CharField(source='photographer.email')
    class Meta:
        model = Posts
        fields = ('id','photographer','photographer_email','photographer_name','image','caption','total_likes')

class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ('likes')
        
class RatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = ('post','comment','rating')