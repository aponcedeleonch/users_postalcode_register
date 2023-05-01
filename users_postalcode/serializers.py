import logging
from rest_framework import serializers
from users_postalcode.models import UserWithAddress, Address

logger = logging.getLogger(__name__)


class UserAndAdress:
    """Helper class to form the objects used by the endpoint."""

    def __init__(self, db_user: UserWithAddress):
        """Fill in the object using a user from the DB."""
        self.id = db_user.id
        self.username = db_user.username
        self.postal_code = db_user.address.postal_code
        self.city = db_user.address.city


class UsersAdressSerializer(serializers.Serializer):
    """Serializer for the UserAndAdress class."""

    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=True, max_length=100)
    postal_code = serializers.CharField(required=True, max_length=10)
    city = serializers.CharField(required=False, max_length=50)

    def create(self, validated_data):
        """Create the address and user in the DB based on the JSON received from the endpoint."""
        username = validated_data.get('username')
        postal_code = validated_data.get('postal_code')
        address = Address(postal_code=postal_code)
        city_of_postal_code = address.get_city_from_address()
        logger.info(f'Found city: {city_of_postal_code} of postal code: {postal_code}.')
        address.save()
        user = UserWithAddress.objects.create(username=username, address=address)
        return UserAndAdress(db_user=user)
