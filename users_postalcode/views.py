from users_postalcode.models import UserWithAddress
from users_postalcode.serializers import UsersAdressSerializer, UserAndAdress
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserList(APIView):
    """Class view meant to respond at /users/."""

    def get(self, request, format=None):
        """Get all users in the DB."""
        users = UserWithAddress.objects.all()
        processed_users = []
        for user in users:
            processed_users.append(UserAndAdress(user))
        serializer = UsersAdressSerializer(processed_users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """Create a new user in the DB."""
        serializer = UsersAdressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """Class view meant to respond at /users/<id>/."""

    def _get_object(self, pk):
        """Get a single user based on the Primary Key."""
        try:
            return UserWithAddress.objects.get(pk=pk)
        except UserWithAddress.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """Get a single user from the DB."""
        user = self._get_object(pk)
        processed_user = UserAndAdress(user)
        serializer = UsersAdressSerializer(processed_user)
        return Response(serializer.data)
