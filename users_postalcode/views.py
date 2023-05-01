from users_postalcode.models import UserWithAddress
from users_postalcode.serializers import UsersAdressSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


def convert_db_user_to_serializer_user(user):
    processed_user = {}
    processed_user['id'] = user.id
    processed_user['username'] = user.username
    processed_user['postal_code'] = user.address.postal_code
    processed_user['city'] = user.address.city
    return processed_user


class UserList(APIView):
    def get(self, request, format=None):
        users = UserWithAddress.objects.all()
        processed_users = []
        for user in users:
            processed_users.append(convert_db_user_to_serializer_user(user))
        serializer = UsersAdressSerializer(processed_users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UsersAdressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def _get_object(self, pk):
        try:
            return UserWithAddress.objects.get(pk=pk)
        except UserWithAddress.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self._get_object(pk)
        processed_user = convert_db_user_to_serializer_user(user)
        serializer = UsersAdressSerializer(processed_user)
        return Response(serializer.data)
