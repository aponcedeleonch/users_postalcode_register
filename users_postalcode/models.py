from django.db import models

class Address(models.Model):
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)

class User(models.Model):
    username = models.CharField(max_length=200)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
