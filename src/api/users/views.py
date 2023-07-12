from django.db import transaction
from django.utils import timezone
from django.conf import settings

from rest_framework.generics import (CreateAPIView, RetrieveAPIView,
                                     DestroyAPIView, ListAPIView)
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


from google.oauth2 import id_token
from google.auth.transport import requests

from api.users.models import Users, Session
from api.users.serializers import UserCreateSerializer, UserListSerializer


class GoogleAuthAPIView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        credential = request.data.get('credential')

        try:
            id_info = self.verify_google_token(credential)
            username, email, google_id = self.get_token_fields(id_info)

            with transaction.atomic():
                user, created = self.get_or_create_user(email,
                                                        username,
                                                        google_id)

                if not created:
                    serializer = self.get_serializer(user)
                    return Response({"user": serializer.data},
                                    status=status.HTTP_200_OK)

                session = self.generate_session(user)
                serializer = self.get_serializer(user)
                return Response({"user": serializer.data},
                                status=status.HTTP_200_OK)
        except ValueError:
            return Response({"message": "Invalid token"},
                            status=status.HTTP_401_UNAUTHORIZED)

    def verify_google_token(self, credential):
        return id_token.verify_oauth2_token(credential, requests.Request())

    def get_token_fields(self, id_info):
        username = id_info.get('name')
        email = id_info.get('email')
        google_id = id_info.get('sub')
        return username, email, google_id

    def get_or_create_user(self, username, email, google_id):
        return Users.objects.get_or_create(google_id=google_id,
                                           defaults={'email': email,
                                                     'username': username})

    def generate_session(self, user):
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        active = True
        generation_date = timezone.now()
        expiration_date = timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        session = Session.objects.create(
            user=user,
            token=token,
            active=active,
            generation_date=generation_date,
            expiration_date=expiration_date
        )
        return session


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = UserCreateSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            session = Session.objects.filter(user=instance).first()
            if session:
                session.check_expiration()
            serializer = self.get_serializer(instance)
            return Response({"user": serializer.data},
                            status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserListAPIView(ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UserListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"users": serializer.data}, status=status.HTTP_200_OK)


class UserDestroyAPIView(DestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UserCreateSerializer

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
