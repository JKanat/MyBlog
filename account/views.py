
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# from .models import MyUser
from .serializers import *
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Successfully sign up", status=status.HTTP_201_CREATED)


class ActivationView(APIView):
    def get(self, email, activation_code):
        user = MyUser.objects.filter(email=email,
                                     activation_code=activation_code).first()
        if not user:
            return Response('This user does not exist', 400)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response('OK', 200)


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Successfully logged out', status=status.HTTP_200_OK)


class ForgotPasswordView(APIView):
    def get(self, request):
        email = request.guery_params.get('email')
        user = get_object_or_404(MyUser, email=email)
        user.is_active = False
        user.save()
        send_activation_code(email=user.email,
                             activation_code=user.activation_code,
                             status='reset_password')
        return Response('Вам отправили письмо на почту')


class CompleteResetPassword(APIView):
    def post(self, request):
        serializer = CreateNewPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Вы успешно поменяли пароль', status=200)
