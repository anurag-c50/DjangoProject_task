from django.shortcuts import render,redirect
from django.http import HttpResponse
from .registerform import Shopform
from .userSearchForm import UserSearch
from .models import Register
from django import forms
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import Shopserializer
from math import radians,cos,sin,sqrt,atan2
# Create your views here.
def clean_latitude(latitude):
    if latitude < -90 or latitude > 90:
        raise forms.ValidationError('Latitude must be between -90 and 90 degrees.')
    return latitude

def clean_longitude(longitude):
    if longitude < -180 or longitude > 180:
        raise forms.ValidationError('Longitude must be between -180 and 180 degrees.')
    return longitude
@api_view(['GET'])
def listofshop(request):
    Shops=Register.objects.all()
    Serializer=Shopserializer(Shops,many=True)
    return Response(Serializer.data)
# @api_view(['POST'])
# def listofshop(request):
#     Shops=Register.objects.all()
#     Serializer=Shopserializer(Shops,many=True)
#     return Response(Serializer.data)

def Registers(request):
    if request.method=='POST':
        form=Shopform(request.POST)
        if form.is_valid():
            clean_longitude(form.cleaned_data['Longitude'])
            clean_latitude(form.cleaned_data['Latitude'])
            form.save()
            return render(request,'viewpage/Notify.html',{'notification':'succesfull'})
    else:
        form=Shopform()
        return render(request,'viewpage/registerform.html',{'form':form})
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    differencelat = radians(lat2 - lat1)
    differencelon = radians(lon2 - lon1)
    A = sin(differencelat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(differencelon / 2) ** 2
    C = 2 * atan2(sqrt(A), sqrt(1 - A))
    return R * C

def UserSerach(request):
    if request.method=='POST':
       form=UserSearch(request.POST) 
       if form.is_valid():
          longitude=form.cleaned_data['longitude']
          latitude=form.cleaned_data['latitude']
          clean_latitude(latitude)
          clean_longitude(longitude)
          Shops = Register.objects.all()
          ShopswWithDistance = [(shop, haversine(latitude, longitude, shop.Latitude, shop.Longitude))
            for shop in Shops
          ]
          SortedShops=sorted(ShopswWithDistance,key=lambda x:x[1])
          return render(request,'viewpage/ListOfShops.html',{'SortedShops':SortedShops})
    else:
       form=UserSearch() 
       return render(request,'viewpage/UserSearch.html',{'form':form})
