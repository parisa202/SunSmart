from django.db import models
from django.utils.text import slugify
from django.urls import reverse
import numpy

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


class PB_AU_CONCERN_V2(models.Model):
    concern = models.CharField(max_length=150, null=True, blank=True)
    gender = models.CharField(max_length=20, choices = GENDER_TYPE, null=True, blank=True)
    age_group = models.CharField(max_length=20, choices = AGE_GROUP, null=True, blank=True)
    percentage = models.FloatField(null=True, blank=True)
    
class PB_AU_VEGGIE_V2(models.Model):
    year = models.IntegerField( null=True, blank=True)
    concern = models.CharField(max_length=150, null=True, blank=True)
    concern_label = models.CharField(max_length=150, null=True, blank=True)
    gender = models.CharField(max_length=20, choices = GENDER_TYPE, null=True, blank=True)
    age_group = models.CharField(max_length=20, choices = AGE_GROUP, null=True, blank=True)
    percentage = models.FloatField(null=True, blank=True)
    margin_error = models.FloatField(null=True, blank=True)    
    
class PB_WHO_BMI_V2(models.Model):
    bmi = models.CharField(max_length=150, null=True, blank=True)
    year = models.IntegerField( null=True, blank=True)
    gender = models.CharField(max_length=20, choices = GENDER_TYPE, null=True, blank=True)
    crude_estimate = models.FloatField(null=True, blank=True)
    

class PAGE_VIEW_V2(models.Model):
    path = models.CharField(max_length=1001, unique=True)
    views = models.IntegerField(default=1)
    
class HEALTH_TAG_V2(models.Model):
    tag = models.CharField(max_length=150, null=True, blank=True)


class DIET_LABEL_V2(models.Model):
    label = models.CharField(max_length=150, null=True, blank=True)


class MEAL_TYPE_V2(models.Model):
    type = models.CharField(max_length=150, null=True, blank=True)


class INGREDIENT_V2(models.Model):
    name = models.CharField(max_length=100)
    food_category = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class NUTRIENTS_V2(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class RECIPES_V2(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField( null=True, blank=True)
    url = models.URLField(max_length=1000)
    total_time = models.CharField(max_length=5, null=True, blank=True)
    serving = models.CharField(max_length=5, null=True, blank=True)
    
    health_tag = models.ManyToManyField(HEALTH_TAG_V2, related_name='recipes_h_v2')
    diet_label = models.ManyToManyField(DIET_LABEL_V2, related_name='recipes_d_v2')
    meal = models.ManyToManyField(MEAL_TYPE_V2, related_name='recipes_m')
    ingredients = models.ManyToManyField(INGREDIENT_V2, through='RECIPE_INGREDIENT_V2')
    nutrients = models.ManyToManyField(NUTRIENTS_V2, through='RECIPE_NUTRIENTS_V2')
    
    slug = models.SlugField(max_length=500, unique=True, null=True, blank=True)
    page_view = models.OneToOneField(PAGE_VIEW_V2, on_delete=models.CASCADE, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        if update_fields is not None and "name" in update_fields:
            update_fields = {"slug"}.union(update_fields)
                          
        # Create or update associated PAGE_VIEW
        if not self.page_view_id:
            page_view, _ = PAGE_VIEW_V2.objects.get_or_create(path=self.get_absolute_url())
            self.page_view = page_view
            
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
        
    def get_absolute_url(self):
        # return urllib.parse.unquote(reverse('CoreAPP:recipe-detail', kwargs={'slug': self.slug}))
        return reverse('V2CoreApp:recipe-detail', kwargs={'slug': self.slug})
        

class RECIPE_INGREDIENT_V2(models.Model):
    recipe = models.ForeignKey(RECIPES_V2, related_name='related_ingredients_v2', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(INGREDIENT_V2, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100, null=True, blank=True)
    measure = models.CharField(max_length=50, null=True, blank=True)
    ingredient_text = models.CharField(max_length=700, null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} {self.measure} of {self.ingredient.name} for {self.recipe}"
    
class RECIPE_NUTRIENTS_V2(models.Model):
    recipe = models.ForeignKey(RECIPES_V2, related_name='related_nutrients_v2', on_delete=models.CASCADE)
    nutrient = models.ForeignKey(NUTRIENTS_V2, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100, null=True, blank=True)
    measure = models.CharField(max_length=50, null=True, blank=True)


    def __str__(self):
        return f"{self.nutrient.name} : {numpy.round(float(self.quantity))} {self.measure} "
    


    