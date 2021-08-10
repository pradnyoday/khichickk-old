from .serializer import UsersSerializer,ProfileSerializer
from accounts.models import Users,Profile

from django.shortcuts import get_object_or_404

from rest_framework import serializers,generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def current_user(request):
    if(request.user.is_authenticated):
        user = request.user
        return Response({
            'username': user.name,
            'email': user.email,
        })
    else:
        return Response({'user':'not logged in '})
        
class GetAllUsersAPIView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    #permission_classes = (IsAdminUser,)

class GetUserAPIView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAdminUser,IsAuthenticated)
    def get(self, request,pk, *args, **kwargs):
        data = Users.objects.get(pk=pk)
        serializer = UsersSerializer(data)
        return Response(serializer.data)

    
class ProfileAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,IsAdminUser)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj

class ProfileDetailAPIView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    
    def get(self, request,email, *args, **kwargs):
        user = Users.objects.get(email=email)
        data = Profile.objects.get(user=user)
        serializer = ProfileSerializer(data)
        return Response(serializer.data)


class FollowAPIView(APIView):
    def get(self,request,pk,*args,**kwargs):
        if(request.user.is_authenticated):
            try:
                current_user_profile = Profile.objects.get(user = request.user)
                current_user = Users.objects.get(pk = request.user.id)
                follow_user = Users.objects.get(pk = pk)
                follow_user_profile = Profile.objects.get(user = follow_user)
                
                current_user_followings = current_user_profile.following.all()
                follow_user_followers = follow_user_profile.followers.all()
                
                try:
                    user_follows = get_object_or_404(current_user_followings,pk=follow_user.id)
                except:
                    user_follows = False
                if(user_follows):
                    current_user_profile.following.remove(follow_user)
                    follow_user_profile.followers.remove(current_user)
                    return Response({'following status':'unfollowed'})
                else:
                    current_user_profile.following.add(follow_user)
                    follow_user_profile.followers.add(current_user)
                    return Response({'following status':'followed'})
                
            except:
                return Response({'request':'invalid'})
        else:
            return Response({'User':'Login Required'})
        
class FollowersListAPIView(generics.ListAPIView):
    def get(self, request,email, *args, **kwargs):
        user = Users.objects.get(email=email)
        profile = Profile.objects.get(user=user)
        data = profile.followers.all()
        d = []
        for i in data:
            d1 = {}
            d1['email'] = i.email
            d1['name'] = i.name
            d.append(d1)
        return Response({'followersList':d})

class FollowingsListAPIView(generics.ListAPIView):
    def get(self, request,email, *args, **kwargs):
        user = Users.objects.get(email=email)
        profile = Profile.objects.get(user=user)
        data = profile.following.all()
        d = []
        for i in data:
            d1 = {}
            d1['email'] = i.email
            d1['name'] = i.name
            d.append(d1)
        return Response({'followingList':d})


from django.shortcuts import render
from django.shortcuts import get_object_or_404

from posts.models import Posts,Ratings
from accounts.models import Users

from .serializer import PostsSerializer,RatingsSerializer
from accounts.serializer import UsersSerializer

from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.response import Response
from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework.views import APIView


class AllPostsAPIView(ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer

class UserAllPostsAPIView(ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    def get(self,request,format=None):
        posts = Posts.objects.filter(photographer=request.user)
        print(posts)
        serializer = PostsSerializer(posts,many=True)
        return Response(serializer.data)

class PostDetailAPIView(APIView):
    def get(self,request,pk,format=None):
        try:
            post = Posts.objects.get(pk=pk)
            serializer = PostsSerializer(post)
            return Response(serializer.data)
        except:
            return Response({'Post':'Unavailable'})       
        
class UploadPostAPIView(CreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    parser_classes = (FormParser, MultiPartParser)

    def post(self, request, *args, **kwargs):
        img = request.data['image']
        photographer = request.user
        post = Posts.objects.create(image=img,photographer=photographer,caption=request.data['caption'])
        return Response({'message': "Uploaded"})

class UserPostsView(ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    def get(self,request,email,format=None):
        try:
            post = Posts.objects.filter(author=Users.objects.get(email=email)).order_by('date')
            serializer = PostsSerializer(post,many=True)
            return Response(serializer.data)
        except:
            return Response({'Post':'Unavailable'})    

class RatingAPIView(ListAPIView):
    queryset = Ratings.objects.all()
    serializer_class = RatingsSerializer

    def post(self, request, *args, **kwargs):
        try:
            post1 = Posts.objects.get(pk = int(request.data['post']))
            rating = int(request.data['rating'])
            comment = request.data['comment']
            user = request.user
            rating = Ratings.objects.create(post=post1,comment=comment,rating=rating,user = user)
            return Response({'Rating Upload Status': "Ok"})
        except:
            return Response({'post':'unavailable'})


    


  
class LikeAPIView(APIView):
    def post(self,request,*args,**kwargs):
        if(request.user.is_authenticated):
            post_id = int(request.data['id'])
            try:
                data = Posts.objects.get(pk = post_id)
                user = request.user
                liked = data.likes.all()
                try:
                    user_liked = get_object_or_404(liked,pk = user.id)
                except:
                    user_liked = False
                if(user_liked):
                    data.likes.remove(user)
                else:
                    data.likes.add(user)
                print(user_liked)
                return Response({'Likes':data.total_likes()})
            except:
                return Response({'post':'unavailable'})
        else:
            return Response({'User':'Login Required'})

class PostLikerAPIView(APIView):
    def get(self,request,pk,format=None):
        try:
            post = Posts.objects.get(pk=pk)
            data = post.likes.all()
            serializer = UsersSerializer(data,many=True)
            return Response(serializer.data)
        except:
            return Response({'Post':'Unavailable'})
        
class CreatePostAPIView(CreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    parser_classes = (FormParser, MultiPartParser)

    def post(self, request, *args, **kwargs):
        img = request.data['image']
        photographer = request.data['photographer']
        post = Posts.objects.create(image=img,photographer=photographer,caption=request.data['caption'])
        return Response({'message': "Uploaded"})