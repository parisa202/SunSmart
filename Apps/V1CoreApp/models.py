from django.db import models

# Create your models here.
GENDER_TYPE = [
    ("M", "Male"),
    ("F", "Female"),
    ("P", "Persons")
]

AGE_GROUP = [
    ("A", "2-3"),
    ("B", "4-8"),
    ("C", "9-13")
]


class PB_AU_CONCERN_V1(models.Model):
    concern = models.CharField(max_length=150, null=True, blank=True)
    gender = models.CharField(max_length=20, choices = GENDER_TYPE, null=True, blank=True)
    age_group = models.CharField(max_length=20, choices = AGE_GROUP, null=True, blank=True)
    percentage = models.FloatField(null=True, blank=True)
    
class PB_WHO_BMI_V1(models.Model):
    bmi = models.CharField(max_length=150, null=True, blank=True)
    year = models.IntegerField( null=True, blank=True)
    gender = models.CharField(max_length=20, choices = GENDER_TYPE, null=True, blank=True)
    crude_estimate = models.FloatField(null=True, blank=True)