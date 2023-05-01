from users_postalcode.models import UserWithAddress
from users_postalcode.serializers import UsersAdressSerializer, UserAndAdress
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserList(APIView):
    def get(self, request, format=None):
        users = UserWithAddress.objects.all()
        processed_users = []
        for user in users:
            processed_users.append(UserAndAdress(user))
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
        processed_user = UserAndAdress(user)
        serializer = UsersAdressSerializer(processed_user)
        return Response(serializer.data)
