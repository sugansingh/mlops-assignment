from django.db import models

#Gender	Age	Smoking	Fatigue	Allergy	Cancer


# Create your models here.
class car(models.Model):
    Car_Name=models.FloatField(max_length=20)
    Year=models.FloatField(max_length=20)
    Present_Price	=models.FloatField(max_length=20)
    Kms_Driven=models.FloatField(max_length=20)
    Fuel_Type=models.FloatField(max_length=20)
    Seller_Type=models.FloatField(max_length=20)
    Transmission=models.FloatField(max_length=20)