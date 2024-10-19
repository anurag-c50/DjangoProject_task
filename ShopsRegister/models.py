from django.db import models

# Create your models here.
class Register(models.Model):
    name = models.CharField(max_length=100, unique=True)  
    owner_name = models.CharField(max_length=100)       
    address = models.TextField()                         
    phone_number = models.CharField(max_length=15, unique=True)  
    email = models.EmailField(unique=True)                
    category = models.CharField(max_length=50)            
    opening_time = models.TimeField()                  
    closing_time = models.TimeField()    
    Longitude=models.FloatField()
    Latitude=models.FloatField()

    def __str__(self):
        return self.name