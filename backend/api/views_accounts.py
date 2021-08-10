from .serializer import UsersSerializer, ProfileSerializer
from accounts.models import Users, Profile

from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework import serializers, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class CreateUserAPIView(generics.CreateAPIView):
    serializer_class = UsersSerializer

class GetAllUsersAPIView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer 

class GetUserAPIView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    def get(self, request, pk):
        queryset = Users.objects.get(pk = pk)
        serializer = UsersSerializer(queryset)
        return Response(serializer.data)

class UpdateUsersAPIView(generics.UpdateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    def get(self, request, pk):
        queryset = Users.objects.get(pk = pk)
        serializer = UsersSerializer(queryset)
        return Response(serializer.data)

class DeleteUsersAPIView(generics.DestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    def get(self, request, pk):
        queryset = Users.objects.get(pk=pk)
        serializer = UsersSerializer(queryset)
        return Response(serializer.data)

from django.views.decorators.csrf import ensure_csrf_cookie

# from django.middleware.csrf import get_token
# def csrf_check(request):
#     return Response({'csrfToken': get_token(request)})

@api_view(['GET','POST'])
@ensure_csrf_cookie
def csrf_check(request):
    i = 1
    if(request.method == 'POST'):
        i = request.data.get('i')
        print(i)
    return Response({'csrfToken': i})