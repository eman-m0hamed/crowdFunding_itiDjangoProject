from rest_framework import generics
from .models import myUser
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from project.models import *
from project.serializers import *

def createToken(userId, duration, role=None):
    payload = {
    'id': userId,
    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=duration),
    'iat': datetime.datetime.utcnow(),
    'role': role
    }
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    return token


def verifyEmailResult(request):
    if request. method == "GET":
        varify = request.GET.get('varify')
        context={}
        context['message'] = varify
        return render(request, 'varifyEmailResult.html', context)

def isLogin(request):
    token =request.META.get('HTTP_AUTHORIZATION')
    if not token:
        raise AuthenticationFailed({"success": False, "message": 'Authentication credentials were not provided.'})
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed({"success": False , "message": 'Token is Expired'})

    except jwt.exceptions.DecodeError:
        raise AuthenticationFailed({"success": False , "message":'Invalid Token'})

    user = myUser.objects.filter(id=payload['id']).first()
    if not user:
        raise AuthenticationFailed({"success": False , "message": 'User Account not found!'})
    elif payload['role'] !="login":
        raise AuthenticationFailed({"success": False , "message": "Invalid Token"})

    return user


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = myUser.objects.all()
    serializer_class = UserSerializer

class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            user = serializer.save()
            token = createToken(userId= user.id,duration=24*60, role="emailVarify")
            current_site = get_current_site(request).domain
            relativeLink = reverse('email-verify')
            absurl = 'http://'+current_site + \
                relativeLink+"?token="+token
            email_body = 'Hi '+user.first_name + \
                ' Use the link below to verify your email \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Verify your email'}
            Util.send_email(data)
            return Response({'success': True, 'msg':'Registration Successfully, View Email Inbox To varify the Email'}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    def post(self, request, *args, **kwargs):
        if 'email' not in request.data and 'password' not in request.data:
          return Response({"success":False, "errors": {"email": ["this field is required"], "password": ["this field is required"]}}, status=status.HTTP_400_BAD_REQUEST)

        elif 'email' not in request.data:
            return Response({"success":False, "errors": {"email": ["this field is required"]}}, status=status.HTTP_400_BAD_REQUEST)

        elif 'password' not in request.data:
            return Response({"success":False, "errors": {"password": ["this field is required"]}}, status=status.HTTP_400_BAD_REQUEST)

        user = myUser.objects.filter(email=request.data['email']).first()

        if user is None:
            return Response({"success": False, "message": "user Account not found!"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(request.data['password']):
            return Response({"success": False, "message": "Incorrect password!"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_verifications:
            return Response({"success": False, "message": "please verify your email"}, status=status.HTTP_401_UNAUTHORIZED)

        token = createToken(userId=user.id, duration=60, role="login")
        return Response({'login': True, 'token': token}, status=status.HTTP_200_OK)


class VarifyEmail(APIView):
    serializer_class = EmailVerificationSerializer
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            if payload['role']!='emailVarify':
                return HttpResponseRedirect(redirect_to='/users/verifyEmailResult/?varify=Invalid Token')

            user = myUser.objects.get(id=payload['id'])
            if not user.is_verifications:
                user.is_verifications = True
                user.save()
                return HttpResponseRedirect(redirect_to='/users/verifyEmailResult/?varify=Email is varified Successfully')
            else:
                return HttpResponseRedirect(redirect_to='/users/verifyEmailResult/?varify=Your Email is alreay varified')

        except jwt.ExpiredSignatureError as identifier:
            return HttpResponseRedirect(redirect_to='/users/verifyEmailResult/?varify=Activation link is Expired')
        except jwt.exceptions.DecodeError as identifier:
            return HttpResponseRedirect(redirect_to='/users/verifyEmailResult/?varify=Invalid Token')


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = myUser.objects.all()
    serializer_class = UserSerializer

class UserProfileView(APIView):
    def get(self, request):
        user = isLogin(request)
        userSerializer = UserSerializer(user)
        return Response({"success": True, "data": userSerializer.data, "message": "user profile data retrieved"})

class userProjectsView(APIView):
    def get(self, request):
        user = isLogin(request)
        userProjects = Project.objects.filter(user=user)
        serializer = ProjectSerializer(userProjects, many=True)
        return Response({"success": True, "data": serializer.data, "message": "All Your Projects are retrieved"})
