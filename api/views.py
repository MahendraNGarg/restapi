
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import generics
from .permissions import IsAuthenticatedOrCreate
from .serializers import (
    RegistrationSerializer, UserLoginSerializer)
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.conf import settings

import json
import subprocess
from rest_framework import viewsets
from .serializers import PostSerializer, CommentSerializer, UserSerializer
from .models import Post, Comment

class SignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (IsAuthenticatedOrCreate,)


class UserActivation(generics.UpdateAPIView):

    def get(self, request, token, user_id, format=None):
        user_obj = User.objects.get(id=user_id)
        token_obj = Token.objects.get(user_id=user_obj)
        if user_obj.is_active == 0:
            if token_obj:
                key = token_obj.key
                if key == token:
                    user_obj.is_active = 1
                    user_obj.save(update_fields=['is_active'])
            serializer = RegistrationSerializer(user_obj)
            serialized_user = serializer.data
            serialized_user['message'] = 'your registration has been activated'
            return HttpResponse(json.dumps(serialized_user), content_type="application/json")
        else:
            serializer = RegistrationSerializer(user_obj)
            serialized_user = serializer.data
            serialized_user['message'] = 'Activation already Done'
            return HttpResponse(json.dumps(serialized_user), content_type="application/json")


class UserAPILoginView (APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, * args, ** kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data

            try:
            	username = User.objects.filter(email=data['email']).first().username
            except Exception as e:
            	username = None

            cmd = 'curl -X POST -d "grant_type=password&username=%s&password=%s" -u "%s:%s" localhost:8000/o/token/' % (
                username, data['password'], settings.CLIENT_ID, settings.CLIENT_SECRET)
            subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

            resp = subprocess.check_output(['bash', '-c', cmd])
            resp = json.loads(resp)
            new_data['access_token'] = resp['access_token']
            new_data['token_type'] = resp['token_type']
            new_data['expires_in'] = resp['expires_in']
            new_data['refresh_token'] = resp['refresh_token']
            new_data['scope'] = resp['scope']
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


def index(request):
	pass


# from rest_framework import viewsets
# from .models import University, Student
# from .serializers import UniversitySerializer, StudentSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer