from django.urls import path
from api.users.views import (GoogleAuthAPIView, UserRetrieveAPIView,
                             UserDestroyAPIView, UserListAPIView)

urlpatterns = [
    path('users/google-auth/', GoogleAuthAPIView.as_view(),
         name='google-auth'),
    path('users/<int:pk>/', UserRetrieveAPIView.as_view(),
         name='user_retrieve'),
    path('users/', UserListAPIView.as_view(),
         name='user_list'),
    path('users/delete/<int:pk>/', UserDestroyAPIView.as_view(),
         name='user_delete'),
]
