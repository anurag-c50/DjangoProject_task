from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns=[
    path("register/",Registers),
    path("userSearch",UserSerach),
    path("list",listofshop)
]