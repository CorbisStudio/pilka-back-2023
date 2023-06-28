from rest_framework.generics import (CreateAPIView, RetrieveAPIView,
                                     DestroyAPIView, ListAPIView)
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from google.oauth2 import id_token
from google.auth.transport import requests

from api.users.models import Users
from api.users.serializers import UserSerializer
from datetime import datetime


class GoogleAuthAPIView(CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        token = request.data.get('token')

        try:
            id_info = self.verify_google_token(token)
            name, email, user_id = self.get_token_fields(id_info)

            with transaction.atomic():
                user, created = self.get_or_create_user(name, email, user_id)
                serializer = self.get_serializer(user)

                if not created:
                    return Response({"user": serializer.data},
                                    status=status.HTTP_409_CONFLICT)

                # Generar el token de sesión
                token = self.generate_token(user)

                response_data = {
                    "session": {
                        "id": user.id,
                        "expiration_date": token["expires_at"],
                        "token": token["token"],
                    },
                    "user": serializer.data
                }

                return Response(response_data,
                                status=status.HTTP_200_OK)
        except ValueError:
            return Response({"message": "Invalid token"},
                            status=status.HTTP_401_UNAUTHORIZED)

    def generate_token(self, user):
        refresh = RefreshToken.for_user(user)
        token = {
            "token": str(refresh.access_token),
            "expires_at": datetime.now() + refresh.access_token.lifetime,
        }
        return token

    def verify_google_token(self, token):
        # Verificar el token de acceso con Google
        return id_token.verify_oauth2_token(token, requests.Request())

    def get_token_fields(self, id_info):
        # Obtener los campos relevantes del token de Google
        name = id_info.get('name')
        email = id_info.get('email')
        user_id = id_info.get('sub')
        return name, email, user_id

    def get_or_create_user(self, name, email, user_id):
        # Verificar si el usuario ya existe en la base de datos o crearlo si no existe
        return Users.objects.get_or_create(user_id=user_id,
                                           defaults={'name': name, 'email': email})


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({"user": serializer.data},
                            status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserListAPIView(ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"users": serializer.data}, status=status.HTTP_200_OK)


class UserDestroyAPIView(DestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "User deleted"},
                            status=status.HTTP_204_NO_CONTENT)
        except Users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def perform_destroy(self, instance):
        instance.delete()
