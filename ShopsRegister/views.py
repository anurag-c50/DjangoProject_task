from django.shortcuts import render,redirect
from .registerform import Shopform
from .userSearchForm import UserSearch
from .models import Register
from django import forms
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import Shopserializer
from math import radians,cos,sin,sqrt,atan2
def clean_latitude(latitude):
    if latitude < -90 or latitude > 90:
        raise forms.ValidationError('Latitude must be between -90 and 90 degrees.')
    return latitude

def clean_longitude(longitude):
    if longitude < -180 or longitude > 180:
        raise forms.ValidationError('Longitude must be between -180 and 180 degrees.')
    return longitude
def validate(data):
    if data['Latitude'] == 0 and data['Longitude'] == 0:
        raise serializers.ValidationError("Latitude and Longitude cannot both be zero.")
    elif data['Longitude'] < -180 or data['Longitude'] > 180:
        raise serializers.ValidationError("Longitude must be between -180 and 180.")
    elif data['Latitude']  < -90 or data['Latitude']  > 90:
        raise serializers.ValidationError('Latitude must be between -90 and 90 degrees.')
    return data
class ShopListCreateView(APIView):
    def get(self, request):
        shop = Register.objects.all()
        serializer = Shopserializer(shop, many=True)
        return Response(serializer.data)

    def post(self, request):
        validate(data=request.data)
        serializer=Shopserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShopSearchView(APIView):
    def haversine_distance(self, lat1, lon1, lat2, lon2):
     R = 6371
     differencelat = radians(lat2 - lat1)
     differencelon = radians(lon2 - lon1)
     A = sin(differencelat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(differencelon / 2) ** 2
     C = 2 * atan2(sqrt(A), sqrt(1 - A))
     return R * C

    def post(self, request):
        latitude = request.data['latitude']
        longitude = request.data['longitude']
        Shops = Register.objects.all()

        ShopDistances = []
        for shop in Shops:
            distance = self.haversine_distance(latitude, longitude, shop.Latitude, shop.Longitude)
            ShopDistances.append({"name": shop.name, "address": shop.address, "distance": distance})

        sorted_shops = sorted(ShopDistances, key=lambda x: x['distance'])
        return Response(sorted_shops)
      
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
