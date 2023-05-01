from django.contrib import admin

from .models import UserWithAddress, Address

admin.site.register(UserWithAddress)
admin.site.register(Address)
