from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.views import APIView

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        token = Token.objects.get(user=user)
        return Response({
            "user": response.data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            return Response({"error": "Invalid credentials"}, status=400)

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key
        })


class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

CustomUser = get_user_model()
users = CustomUser.objects.all()

class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if target_user == request.user:
            return Response({"error": "You cannot follow yourself"}, status=400)

        request.user.following.add(target_user)
        return Response({"message": f"You are now following {target_user.username}"})


class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        request.user.following.remove(target_user)
        return Response({"message": f"You unfollowed {target_user.username}"})
