from rest_framework import serializers
from api.users.models import Users, Session


class UserCreateSerializer(serializers.ModelSerializer):
    session = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ('id', 'email', 'username', 'session')

    def get_session(self, user):
        session = Session.objects.get(user=user)
        return {
            "id": session.id,
            "token": session.token,
            "active": session.active,
            "generation_date": session.generation_date,
            "expiration_date": session.expiration_date,
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('id', 'email', 'username')
