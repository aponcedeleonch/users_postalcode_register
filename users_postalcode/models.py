import os
import requests
from django.db import models
from django.conf import settings


GEONAMES_USERNAME = getattr(settings, "GEONAMES_USERNAME", None)

class Address(models.Model):
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self):
        return f"{self.postal_code} - {self.city}"
    
    def get_city_from_address(self):
        payload = {'postalcode': self.postal_code, 'country': 'ES', 'username': GEONAMES_USERNAME}
        response = requests.get('http://api.geonames.org/postalCodeLookupJSON', params=payload) 

        if response.status_code != requests.codes.ok:
            raise RuntimeError(f"Could not find Postal Code: {self.postal_code}")

        response_dict = response.json()
        if "postalcodes" not in response_dict:
            raise RuntimeError(f"Received strange response from Geonames API: {response_dict}")
        
        self.city = response_dict["postalcodes"][0]['adminName3']
        return self.city


class UserWithAddress(models.Model):
    username = models.CharField(max_length=200, null=False, blank=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.username
