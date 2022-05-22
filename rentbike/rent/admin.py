from django.contrib import admin

# Register your models here.
from rent.models import BikeType, Bike, Reservation
admin.site.register(BikeType)
admin.site.register(Bike)
admin.site.register(Reservation)


