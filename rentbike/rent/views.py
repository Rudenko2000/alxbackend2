from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context
from rent.models import Bike,BikeType,Reservation
from rent.forms import ReservationForm
from django.contrib import messages
from django.urls import reverse



# Create your views here.

def home(request):
    context = {
            'Byketypes': BikeType.objects.all()
        }
    return render(request, "rent/home.html", context)

def reservation(request, biketype_id):
    form=ReservationForm(request.POST)
    context = {
        "biketype": get_object_or_404(BikeType, id=biketype_id),
        "form": ReservationForm(request.POST),
    }
    if request.method == "POST":
        if form.is_valid():
            biketype=BikeType.objects.get(id=biketype_id)
            date = form.cleaned_data["date"]
            client = form.cleaned_data["client"]


            bike = biketype.get_wolny_rower(date)

            if type(bike)==Bike:
                reservation = Reservation(bike=bike, date=date, client=client)
                reservation.save()

                messages.add_message(request, messages.SUCCESS, 'rezerwacja pomyślnie zakończona')
                return HttpResponseRedirect(reverse('reservation_page', args=(reservation.id,)))
            else:
                messages.add_message(request,messages.ERROR, 'brak dostępnych rowerów na ten dzień,'
                                                             ' wybierz inny typ lub inny dzień')

    return render(request, 'rent/biketype.html', context)

def reservation_page(request, reservation_id):
    reservation=Reservation.objects.get(id=reservation_id)
    context = {

        "data": reservation.date,
        "client": reservation.client,
        "numer_ramy": reservation.bike.numer_ramy,
        "typ_roweru": reservation.bike.type.type,
        "reservation_id":reservation_id

    }
    return render(request, 'rent/reservation.html', context)






