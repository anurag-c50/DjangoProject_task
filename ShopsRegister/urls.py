from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns=[
    path("register/",Registers),
    path("userSearch/",userSearch),
    path('', ShopListCreateView.as_view()),
    path('search', ShopSearchView.as_view()),

]