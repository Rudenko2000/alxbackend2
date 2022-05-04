"""rentbike URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
import rent.views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',rent.views.index,name="home"),
    path('rower/<int:biketype_id>',rent.views.reservation,name="rower"),
    path('rent/<int:reservation_id>',rent.views.reservation_page,name="reservation_page")

]
