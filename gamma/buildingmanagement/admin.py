from django.contrib import admin
from buildingmanagement.models import Room, Reservation, Projector, Accesscard
# Register your models here.

admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Projector)
admin.site.register(Accesscard)


