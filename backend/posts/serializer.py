from .models import Posts,Ratings
from rest_framework import serializers

        
class PostsSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name')
    author_email = serializers.CharField(source='author.email')
    class Meta:
        model = Posts
        fields = ('id','author_email','author_name','image','caption','total_likes')

class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ('likes')
        
class RatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = ('post','comment','rating')