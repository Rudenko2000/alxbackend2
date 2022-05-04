from django import forms
from django.core.exceptions import ValidationError
from .models import BikeType, Bike, Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model=Reservation
        exclude=('bike',)
        fields=("date","client")



