from django.db import models
from django.db import transaction
from django.db.models import F, UniqueConstraint, CheckConstraint
from django.contrib.auth.models import User

from django.conf import settings

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=100)
    people_count = models.PositiveSmallIntegerField(default=0)
    max_people_count = models.PositiveSmallIntegerField(null=False)
    image = models.ImageField(upload_to="images/", null=True)


    def get_accesscards(self):
        return Accesscard.objects.filter(room=self)
    def __str__(self):
        return self.name

    def get_reserved_days(self,month):
        return Reservation.objects.filter(room=self).\
            filter(date__month=month).values_list('date__day', flat=True)



    @transaction.atomic
    def move_people_to(self, other_room, count=1):
        #### Nie odporne na równoległy zapis w bazie
        # self.people_count -= count
        # self.save()
        # other_room.people_count += count
        # other_room.save()

        #Room.objects.filter(id=self.id).update(people_count=F("people_count") - count)
        #Room.objects.filter(id=other_room.id).update(people_count=F("people_count") + count)
        # albo:
        # self.people_count = F("people_count") - count
        # self.save()
        # other_room.people_count = F("people_count") + count
        # other_room.save()
        # # ale uwaga: powysze pozostawia obiekt F w self.people_coun,
        # # więc kolejny self.save znów mniejszy wartość.
        # # Dopiero self.refresh_from_db() wyczyści nam to pole

        ### inne podejście do radzenia sobie z równoległymi zapisami do bazy (blokuje do końca transakcji)
        Room.objects.filter(id=self.id).select_for_update()
        Room.objects.filter(id=other_room.id).select_for_update()
        self.people_count -= count
        self.save()
        other_room.people_count += count
        other_room.save()

        ### inny sposób użycia transakcji:
        # with transaction.atomic():
        #     self.people_count -= count
        #     self.save()
        #     other_room.people_count += count
        #     other_room.save()



class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    # user = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = [
            ["room","date","user"],
            ["date", "user"]
        ]
        # constraints= [
        #     CheckConstraint(check=..., name="people_count_maximum")
        # ]


    def __str__(self):
        return f"{self.user} / {self.room.name} / {self.date}"


class Projector(models.Model):
    producer=models.CharField(max_length=100)
    serial_number=models.CharField(max_length=100)
    room=models.OneToOneField(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.producer}, {self.serial_number}"

class Accesscard(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE

    )
    room = models.ManyToManyField(Room, related_name="accesscards")

    def __str__(self):
        return f"{self.owner}'s card {self.id}"

class UserProfile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )


