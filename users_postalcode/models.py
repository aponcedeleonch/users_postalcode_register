import requests
from django.db import models
from django.conf import settings


GEONAMES_USERNAME = getattr(settings, "GEONAMES_USERNAME", None)

class Address(models.Model):
    """Detail table in the DB with the postal code and the city."""
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self):
        """String representation from Address."""
        return f"{self.postal_code} - {self.city}"
    
    def get_city_from_address(self):
        """Get the city based on the address using geonames API."""
        # Note that geonames user is needed to use the free API of geonames.
        # The username should be specified in a .env file located at the top of the project.
        payload = {'postalcode': self.postal_code, 'country': 'ES', 'username': GEONAMES_USERNAME}
        response = requests.get('http://api.geonames.org/postalCodeLookupJSON', params=payload) 

        if response.status_code != requests.codes.ok:
            raise RuntimeError(f"Could not find Postal Code: {self.postal_code}")

        response_dict = response.json()
        if "postalcodes" not in response_dict:
            raise RuntimeError(f"Received strange response from Geonames API: {response_dict}")

        # Getting only the city from the response.
        self.city = response_dict["postalcodes"][0]['adminName3']
        return self.city


class UserWithAddress(models.Model):
    """User table in the DB."""
    username = models.CharField(max_length=200, null=False, blank=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        """String representation from UserWithAddress."""
        return self.username
