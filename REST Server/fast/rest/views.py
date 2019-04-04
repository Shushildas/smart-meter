from django.shortcuts import render
from rest_framework.views import APIView
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate
from .models import Profile, Record, Bill
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, ProfileSerializer, RecordsSerializer, BillSerializer
from rest_framework.authtoken.models import Token
from django.core import serializers
from django.utils.timezone import utc
import datetime
# Create your views here.
TIME_DIFF = 5


def save_in_bill(request):
    new_request = request.copy()
    new_request['cost'] = request['energy'] * 14
    serializer = BillSerializer(new_request)
    if serializer.is_valid():
        serializer.save()
    else:
        raise serializers.ValidationError({'Cannot Save Bill'})


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class ProfileCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ProfileSerializer


class ProfileAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        user_profile = get_object_or_404(Profile, user=user)
        data = ProfileSerializer(user_profile).data
        return Response(data)

    def put(self, request, username):
        user = get_object_or_404(User, username=username)
        user_profile = get_object_or_404(Profile, user=user)
        serialize = ProfileSerializer(user_profile, data=request.data)
        if serialize.is_valid():
            serialize.save()
            Response(status=200)
        return Response(status=404)

    def delete(self, request, username):
        user = get_object_or_404(User, username=username)
        user_profile = get_object_or_404(Profile, user=user)
        user_profile.delete()
        user.delete()
        return Response(status=200)


class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, format=None):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=401)


class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = ()


class RecordListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(Profile, user=user)
        records = get_list_or_404(Record, profile=profile)
        serialize = RecordsSerializer(records, many=True)
        return Response(serialize.data, status=200)

    def post(self, request, username):
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(Profile, user=user)
        request.data['profile'] = profile.id
        try:
            if(request['bill_time'] == 1):
                save_in_bill(request)
            request.pop('bill_time')
            serialize = RecordsSerializer(request.data)
            if serialize.is_valid():
                serialize.save()
                return Response(serialize.data, status=200)
        except serializers.ValidationError:
            return Response(400)
        return Response(serialize.errors, status=400)


class BillListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        bills = get_list_or_404(Bill)
        serialize = BillSerializer(bills, many=True)
        return Response(serialize.data, status=200)
