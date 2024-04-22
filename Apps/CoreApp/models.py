from django.db import models


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


class PB_AU_CONCERN(models.Model):
    concern = models.CharField(max_length=150, null=True, blank=True)
    gender = models.CharField(max_length=20, choices = GENDER_TYPE, null=True, blank=True)
    age_group = models.CharField(max_length=20, choices = AGE_GROUP, null=True, blank=True)
    percentage = models.FloatField(null=True, blank=True)
    
class PB_WHO_BMI(models.Model):
    bmi = models.CharField(max_length=150, null=True, blank=True)
    year = models.IntegerField( null=True, blank=True)
    gender = models.CharField(max_length=20, choices = GENDER_TYPE, null=True, blank=True)
    crude_estimate = models.FloatField(null=True, blank=True)
    

class HEALTH_TAG(models.Model):
    tag = models.CharField(max_length=150, null=True, blank=True)

class MEAL_TYPE(models.Model):
    type = models.CharField(max_length=150, null=True, blank=True)
    
class RECIPES(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    description = models.TextField( null=True, blank=True)
    health_tag = models.ManyToManyField(HEALTH_TAG, related_name='recipes_h')
    meal = models.ManyToManyField(MEAL_TYPE, related_name='recipes_m')


