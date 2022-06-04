from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(),  name="home"),
    path('reserve', views.reserve, name='reserve'),
    path("signup", views.signup, name="signup"),
    path('roomview/<int:room_id>',views.roomview,name="roomview"),
    path('reservations',views.ReservationListView.as_view(),name="reservations"),
    path('roomlist',views.RoomlistView.as_view(), name="roomlist"),
    path('roomview/add',views.AddRoom.as_view(), name="add_room"),
]