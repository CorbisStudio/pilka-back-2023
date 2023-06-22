from django.urls import path
from api.users.views import (GoogleAuthAPIView, UserRetrieveAPIView,
                             UserDestroyAPIView, UserListAPIView)

urlpatterns = [
    path('users/auth/', GoogleAuthAPIView.as_view(), name='user_create'),
    path('users/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_retrieve'),
    path('users/delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user_delete'),
    path('users/', UserListAPIView.as_view(), name='user_list'),
]