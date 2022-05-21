from django.db import models
from django.db import transaction
from django.db.models import F

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=100)
    people_count=models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name


    @transaction.atomic
    def move_people_to(self, other_room, count=1):

        Room.objects.filter(pk=self.pk).update(people_count = F("people_count") - count)
        self.people_count -= count
        self.save()
        other_room.people_count += count
        other_room.save()

        """żeby uzyć transaction.atomiv do częsci codu:"""

        # with transaction.atomic():
        #     self.people_count -= count
        #     self.save()
        #     other_room.people_count += count
        #     other_room.save()


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    user = models.CharField(max_length=255)


    def __str__(self):
        return f"{self.room.name} / {self.date}"



