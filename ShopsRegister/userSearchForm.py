from django import forms

class UserSearch(forms.Form):
       longitude = forms.FloatField(label="Enter Longitude",widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Longitude'}))
       latitude = forms.FloatField(label="Enter Latitude",widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Latitude'}))