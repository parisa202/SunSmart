from django.db import models
from django.utils.text import slugify
from django.urls import reverse


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
    
class PB_AU_VEGGIE(models.Model):
    year = models.IntegerField( null=True, blank=True)
    concern = models.CharField(max_length=150, null=True, blank=True)
    concern_label = models.CharField(max_length=150, null=True, blank=True)
    gender = models.CharField(max_length=20, choices = GENDER_TYPE, null=True, blank=True)
    age_group = models.CharField(max_length=20, choices = AGE_GROUP, null=True, blank=True)
    percentage = models.FloatField(null=True, blank=True)
    margin_error = models.FloatField(null=True, blank=True)    
    
class PB_WHO_BMI(models.Model):
    bmi = models.CharField(max_length=150, null=True, blank=True)
    year = models.IntegerField( null=True, blank=True)
    gender = models.CharField(max_length=20, choices = GENDER_TYPE, null=True, blank=True)
    crude_estimate = models.FloatField(null=True, blank=True)
    

class HEALTH_TAG(models.Model):
    tag = models.CharField(max_length=150, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Check for duplicates before saving
        if HEALTH_TAG.objects.filter(tag=self.tag).exists():
            return
        super().save(*args, **kwargs)

class DIET_LABEL(models.Model):
    label = models.CharField(max_length=150, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Check for duplicates before saving
        if DIET_LABEL.objects.filter(tag=self.tag).exists():
            return
        super().save(*args, **kwargs)

class MEAL_TYPE(models.Model):
    type = models.CharField(max_length=150, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Check for duplicates before saving
        if MEAL_TYPE.objects.filter(type=self.type).exists():
            return
        super().save(*args, **kwargs)

class INGREDIENT(models.Model):
    name = models.CharField(max_length=100)
    food_category = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class RECIPES(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    description = models.TextField( null=True, blank=True)
    health_tag = models.ManyToManyField(HEALTH_TAG, related_name='recipes_h')
    diet_label = models.ManyToManyField(DIET_LABEL, related_name='recipes_d')
    url = models.URLField(max_length=200)
    meal = models.ManyToManyField(MEAL_TYPE, related_name='recipes_m')
    slug = models.SlugField(unique=True, null=True, blank=True)
    ingredients = models.ManyToManyField(INGREDIENT, through='RECIPE_INGREDIENT')
    

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.slug = slugify(self.name)
        if update_fields is not None and "name" in update_fields:
            update_fields = {"slug"}.union(update_fields)
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
        
    def get_absolute_url(self):
        # return urllib.parse.unquote(reverse('CoreAPP:recipe-detail', kwargs={'slug': self.slug}))
        reverse('CoreApp:recipe-detail', kwargs={'slug': self.slug})
        

class RECIPE_INGREDIENT(models.Model):
    recipe = models.ForeignKey(RECIPES, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(INGREDIENT, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)
    measure = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.quantity} {self.measure} of {self.ingredient.name} for {self.recipe}"