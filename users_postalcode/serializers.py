from rest_framework import serializers
from users_postalcode.models import UserWithAddress, Address

class UsersAdressSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=True, max_length=100)
    postal_code = serializers.CharField(required=True, max_length=10)
    city = serializers.CharField(required=True, max_length=50)

    def create(self, validated_data):
        username = validated_data.get('username')
        city = validated_data.get('city')
        postal_code = validated_data.get('postal_code')
        address = Address.objects.create(city=city, postal_code=postal_code)
        return UserWithAddress.objects.create(username=username, address=address)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.id = validated_data.get('id', instance.id)
        instance.username = validated_data.get('username', instance.username)
        instance.postal_code = validated_data.get('postal_code', instance.postal_code)
        instance.city = validated_data.get('city', instance.city)
        instance.save()
        return instance
