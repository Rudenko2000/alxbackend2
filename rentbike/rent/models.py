import random

from django.db import models
from datetime import date


# Create your models here.

class BikeType(models.Model):
    type=models.CharField(max_length=50)
    opis=models.TextField()
    def get_wolny_rower(self,date):

        bikes = Bike.objects.filter(type=self).exclude(reservation__date=date)
        if (bikes):
             bike = random.choice(bikes)
        else:
            bike=None
        return bike

class Bike(models.Model):
    type=models.ForeignKey(BikeType, on_delete=models.CASCADE)
    numer_ramy=models.CharField(max_length=15)

class Reservation(models.Model):
    bike=models.ForeignKey(Bike,on_delete=models.CASCADE)
    date=models.DateField(default=date.today)
    client=models.CharField(max_length=30)
    def __str__(self):
        return f"bike {self.bike} pk: {self.bike.pk} {self.bike.numer_ramy}date {self.date}, client {self.client}"


