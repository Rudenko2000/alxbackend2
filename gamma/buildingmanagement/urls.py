from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('reserve', views.reserve, name='reserve'),
    path("signup", views.signup, name="signup"),
    path('roomview/<int:room_id>',views.roomview,name="roomview"),
    path('reservations',views.reservations,name="reservations"),

]