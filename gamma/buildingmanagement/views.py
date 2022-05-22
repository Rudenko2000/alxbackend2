
from django.contrib.auth import login, authenticate
from django.db import IntegrityError
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib import messages


from .models import Reservation, Room
from buildingmanagement.forms import ReservationForm

# Create your views here.
@login_required
def home(request):
    context = {
        'Rooms': Room.objects.all()
    }
    return render(request,"buildingmanagement/home.html",context)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def reserve(request):
    form = ReservationForm(request.POST)
    if request.method == "POST":

        if form.is_valid():
            room =form.cleaned_data["room"]
            date = form.cleaned_data["date"]
            user = request.user

            reservation = Reservation(
                    room=room,
                    date=date,
                    user=user
                )
            try:
                reservation.save()
            except IntegrityError as e:
                ...
                messages.add_message(request, messages.ERROR, f'ta rezerwacja dla {user} na {date} już istnieje  {e}')

            else:
                messages.add_message(request, messages.SUCCESS, f'rezerwacja pomyślnie zakończona {user} {room.name} {date}')
                return redirect(home)
    else:
          form = ReservationForm()
    return render(request, "buildingmanagement/room.html", {'form': form})

# @login_required
# def reserve(request):
#     if request.method == "POST":
#         form = ReservationForm(request.POST)
#         if form.is_valid():
#             reservation = Reservation(
#                 room=form.cleaned_data["room"],
#                 date=form.cleaned_data["date"],
#                 user=request.user
#             )
#             try:
#                 reservation.save()
#             except IntegrityError as e:
#                 # TODO: sprawdzenie czy to na pewno ten constraint
#                 # np. e.args: ('UNIQUE constraint failed: buildingmanagement_reservation.room_id, buildingmanagement_reservation.date',)
#                 form.add_error("date", "Room already taken")
#             else:
#                 return redirect("home")
#     else:
#         form = ReservationForm()
#     return render(request, 'buildingmanagement/room.html', {'form': form})




def reservations(request):

    return render(request, "buildingmanagement/reservation.html", {"reservations":Reservation.objects.all()})



#@login_required  - do użycia dla function-based-views

class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation

def roomview(request, room_id):
    room=get_object_or_404(Room, id=room_id)
    reserved_days=room.find_reserved_days(month=5)
    return render(request, "buildingmanagement/roomview.html", {"room": room,'reserved_days':reserved_days})
