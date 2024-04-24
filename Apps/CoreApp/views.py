from typing import Any
from django.http.request import HttpRequest as HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.core.mail import send_mail
from django.core.management.utils import get_random_secret_key
from django.views.generic.detail import DetailView
from django.utils.text import slugify
from django.views.generic.detail import DetailView
from .models import *
from django.apps import apps
import os
from .utils import api_request, login_required
import pandas as pd
from django.core import serializers
import json
import requests
from django.db.models import Q
from functools import reduce
from operator import or_


class CustomLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if 'user_id' not in request.session:
            # Redirect to the login page
            messages.add_message(self.request, messages.INFO, 'You need to login to access the content')
            # Store the requested URL in the session
            request.session['next'] = request.get_full_path()
            return redirect('CoreApp:login_or_register')
        return super().dispatch(request, *args, **kwargs)
    
    
class HomeView(generic.TemplateView):
    template_name = 'CoreApp/index.html'
    
    def import_data(self):
        filename = "C:/Users/Parisa/Downloads/tb_concern.csv"
        df = pd.read_csv(filename)
        for index, row in df.iterrows():
            temp_row = PB_AU_CONCERN(concern=row['concern'], 
                                        gender=row['gender'],
                                        age_group=row['age_group'],
                                        percentage=row['percentage'])
            
            temp_row.save()
    
    def import_bmi_data(self):
        filename = "C:/Users/Parisa/Downloads/pb_who_bmi.csv"
        df = pd.read_csv(filename)
        for index, row in df.iterrows():
            temp_row = PB_WHO_BMI(bmi=row['bmi_code'], 
                                        gender=row['gender'],
                                        year=row['year'],
                                        crude_estimate=row['crude_estimate'])
            
            temp_row.save()
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        # self.import_bmi_data()
            
        return super().get_context_data(**kwargs)

#overweight info page    
class US11View(generic.TemplateView):
    template_name = 'CoreApp/overweight.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        super().get_context_data(**kwargs)
        
        # query from table
        all_data = PB_AU_CONCERN.objects.all()
        serialized_data = serializers.serialize('json', all_data)
        
        
        all_data_bmi = PB_WHO_BMI.objects.all()
        serialized_data_bmi = serializers.serialize('json', all_data_bmi)
    
        
        new_context = {'main_title': 'Obesity and Overweight among Children',
                    #    'sub_title': 'Obesity and Overweight among Children',
                       'page_name': 'Obesity and Overweight',
                       'json_data': serialized_data,
                       'json_data_bmi': serialized_data_bmi}
        
        return new_context
        

class US11DashboardView(generic.TemplateView):
    template_name = 'CoreApp/us11_dashboard.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        super().get_context_data(**kwargs)
        
        # query from table
        all_data = PB_AU_CONCERN.objects.all()
        serialized_data = serializers.serialize('json', all_data)
        
        
        all_data_bmi = PB_WHO_BMI.objects.all()
        serialized_data_bmi = serializers.serialize('json', all_data_bmi)
    
        
        new_context = {'main_title': 'Checkout',
                       'sub_title': 'Shop',
                       'page_name': 'US11',
                       'json_data': serialized_data,
                       'json_data_bmi': serialized_data_bmi}
        
        return new_context
 
    
class US121View(generic.TemplateView):
    template_name = 'CoreApp/us121.html'


class US13View(generic.TemplateView):
    template_name = 'CoreApp/additive.html'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        super().get_context_data(**kwargs)
        
        
    
        
        new_context = {'main_title': 'Understanding Food Additives: Uses, Reactions, and Safety',
                       'sub_title': '',
                       'page_name': 'Understanding Food Additives'
                       }
        
        return new_context

#nutrition-guideline
class US21View(generic.TemplateView):
    template_name = 'CoreApp/nutrition-guideline.html'
    data = ""
    
    #read json guideline
    def setup(self, request, *args, **kwargs):
        file_address = os.path.join('Data Sources', 'guideline.json')
        with open(file_address, 'r') as f:
            # JSON to dictionary
            self.data = json.load(f)
            
        return super().setup(request, *args, **kwargs)
    
    #search age
    def post(self, request):
        selected_age_range = request.POST.get('selected_age_range')  
        print(selected_age_range) 
        # find the recipe in recipes
        for r in self.data:
            if r.get('age_range') == selected_age_range:
                age_range = r
                print(age_range)
                break
            else:
                age_range = {'status': 'not found'}
                
        return JsonResponse(age_range)            
              
                
class US22View(generic.TemplateView):
    template_name = 'CoreApp/us22.html'

#Reminder page
class ReminderView(generic.TemplateView):
    template_name = 'CoreApp/reminder_main.html'
    
    def post(self, request):
        email = request.POST.get('email', None)
        date = request.POST.get('date', None)
        meal = request.POST.get('meal', None)
        
        # send sign-in data to authentication API
        api_url = 'http://juniorjoy.site/api/reminder/set-ses-reminder'
        
        data = {'email': email,
                'date': date,
                'meal': meal
        }
        response = api_request(url=api_url, parameters=data, request_type='POST')    
       
        messages.add_message(self.request, messages.SUCCESS, 'The reminder has been set successfully  ')
        
        return redirect('CoreApp:US23')
        
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        super().get_context_data(**kwargs)
  
        new_context = {'main_title': 'Reminder',
                       'sub_title': '',
                       'page_name': 'Reminder'
        }
        
        return new_context


class AboutUsView(generic.TemplateView):
    template_name = 'CoreApp/about_us.html'


# class GuestTrackerView(CustomLoginRequiredMixin, generic.TemplateView):
class GuestTrackerView(generic.TemplateView):
    template_name = 'CoreApp/Nutrition_Analysis.html'
    recipes = None
    headers = {
                "Content-Type": "application/json"
                }
    
    def setup(self, request, *args, **kwargs):
        file_address = os.path.join('Data Sources', 'recipes.json')
        with open(file_address, 'r') as f:
            # JSON to dictionary
            self.recipes = json.load(f)
            
        return super().setup(request, *args, **kwargs)
    
    def post(self, request):
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            selected_recipe = request.POST.get('selected_recipe')
            recipe_intake = request.POST.get('recipe_intake')
                            
            # find the recipe in recipes
            for r in self.recipes:
                if r.get('recipe_name') == selected_recipe:
                    recipe = r
                    break
                else:
                    recipe = {'status': 'not found'}
                    
            # send sign-in data to authentication API
            api_url = 'https://juniorjoy.site/api/api/calcucalories'
            data = {
                "query": recipe['recipe_ingredients'],
                "intake": recipe_intake,
                "serving": recipe['recipe_servings']
            }
                        
            response = requests.get(api_url, headers=self.headers, json=data)
            
            if response.status_code == 200:
                # Append the calorie information to the recipe
                recipe['nutrient_info'] = response.json()            
                response_data = response.json()

                recipe['calories_intake'] = response_data['calories_intake']
                recipe['serving_size_g_intake'] = response_data['serving_size_g_intake']
                recipe['fat_total_g_intake'] = response_data['fat_total_g_intake']
                recipe['fat_saturated_g_intake'] = response_data['fat_saturated_g_intake']
                recipe['protein_g_intake'] = response_data['protein_g_intake']
                # recipe['sodium_mg_intake'] = response_data['sodium_mg_intake']
                # recipe['potassium_mg_intake'] = response_data['potassium_mg_intake']
                # recipe['cholesterol_mg_intake'] = response_data['cholesterol_mg_intake']
                recipe['carbohydrates_total_g_intake'] = response_data['carbohydrates_total_g_intake']
                recipe['fiber_g_intake'] = response_data['fiber_g_intake']
                recipe['sugar_g_intake'] = response_data['sugar_g_intake']

            else:
                # Handle API error
                recipe['nutrient_info'] = {'error': 'Failed to retrieve calorie information'}
                    
            return JsonResponse(recipe)
        
        # Not AJAX request
        else:
            submit_data = request.POST.get('submit_data', None)
            messages.add_message(self.request, messages.SUCCESS, 'The information saved successfully')
            return redirect('CoreApp:guest_tracker')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        return {'recipes': self.recipes}  


class MacronutrientsView(generic.TemplateView):
    template_name = 'CoreApp/Macronutrients.html'
    macro_info = None
    
    def setup(self, request, *args, **kwargs):
        file_address = os.path.join('Data Sources', 'macro-info.json')
        with open(file_address, 'r') as f:
            # JSON to dictionary
            self.macro_info = json.load(f)
        return super().setup(request, *args, **kwargs)
    
    
    def post(self, request):
        selected_tag = request.POST.get('selected_tag')
        
        # find 
        for r in self.macro_info['macronutrients']:
            if r.get('name') == selected_tag:
                info = r
                break
            else:
                info = {'status': 'not found'}
        return JsonResponse(info)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        super().get_context_data(**kwargs)
        # tags = ['fashion', 'style', 'CARBOHYDRATES', 'PROTEIN', 'travel', 'shopping', 'hobbies']
        new_context = {'main_title': 'Understanding Macronutrients for Children',
                       'sub_title': '',
                       'page_name': 'Understanding Macronutrients'
                       }
        
        return new_context

    
class MicronutrientsView(generic.TemplateView):
    template_name = 'CoreApp/Micronutrients.html'
    micro_info = None
    
    def setup(self, request, *args, **kwargs):
        file_address = os.path.join('Data Sources', 'micro-info.json')
        with open(file_address, 'r') as f:
            # JSON to dictionary
            self.micro_info = json.load(f)
        return super().setup(request, *args, **kwargs)
    
    
    def post(self, request):
        selected_tag = request.POST.get('selected_tag')
        
        # find 
        for r in self.micro_info['micronutrients']:
            if r.get('name') == selected_tag:
                info = r
                break
            else:
                info = {'status': 'not found'}
        return JsonResponse(info)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        super().get_context_data(**kwargs)
        # tags = ['fashion', 'style', 'CARBOHYDRATES', 'PROTEIN', 'travel', 'shopping', 'hobbies']
        new_context = {'main_title': 'Understanding Micronutrients for Children',
                       'sub_title': '',
                       'page_name': 'Understanding Micronutrients'
                       }
        
        return new_context
    

class RecipeDetailView(DetailView):
    model = RECIPES
    template_name = 'CoreApp/recipe_detail.html'
    slug_field = 'slug'
    
    # # Access ingredients for a recipe
    # ingredients_for_recipe = RECIPES.ingredients.all()
    # for ingredient in ingredients_for_recipe:
    #     print(f"{ingredient.name}: {RECIPE_INGREDIENT.objects.get(recipe=RECIPES, ingredient=ingredient).quantity}")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the current recipe object
        recipe = self.get_object()

        # Include recipe health tags in context
        context['health_tags'] = recipe.health_tag.all()

        # Include recipe diet labels in context
        context['diet_labels'] = recipe.diet_label.all()

        # Include recipe ingredients in context
        context['ingredients'] = recipe.ingredients.all()

        return context


class RecipeListView(generic.ListView):
    template_name = 'CoreApp/recipe_list.html'
    model = RECIPES
    context_object_name = 'all_recipes'
    all_selected_options = None
       
    def get_queryset(self):
        queryset = super().get_queryset()
        self.all_selected_options = []
        
        # GET parameters from the request 
        health_tag = self.request.GET.getlist('health_tag')
        meal = self.request.GET.getlist('meal')
        
        self.all_selected_options.extend(health_tag)
        self.all_selected_options.extend(meal)
        
        # Filter queryset based on parameters
        if not (health_tag=='' or health_tag==[] or health_tag==None):
            tempQuery = reduce(or_, (Q(health_tag__tag__exact=t) for t in health_tag))
            queryset = queryset.filter(tempQuery)
            
        if not (meal=='' or meal==[] or meal==None):
            tempQuery = reduce(or_, (Q(meal__type__exact=t) for t in meal))
            queryset = queryset.filter(tempQuery)
            
        self.queryset = queryset
        return queryset
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        # query from table
        all_recipes_count = self.queryset.count()
        
        context.update({'main_title': 'Healthy Recipes',
                       'page_name': 'Healthy Recipes',
                       'all_recipes_count' : all_recipes_count,
                       'selected_options': self.all_selected_options
                       })
        
        return context
    

class OuterRecipeAnalysisView(generic.TemplateView):
    template_name = 'CoreApp/outer_recipe_analysis.html'


class ComingView(generic.TemplateView):
    template_name = 'CoreApp/coming_soon.html'


class ImportDataView(generic.View):
    def get(self, request, *args, **kwargs):
        file_name = request.GET.get('file_name')
        model_name = request.GET.get('model_name')
        
        # grab the model class using its name
        model_class =  apps.get_model('CoreApp', model_name)
        
        # Files are stored in a folder named 'Data Sources' within your Django project directory
        file_address = os.path.join('Data Sources', file_name)
        
        try:
            df = pd.read_csv(file_address)
            if model_class:
                for index, row in df.iterrows():
                    
                    # model PB_WHO_BMI
                    if model_name == 'PB_WHO_BMI':
                        model_class.objects.create(
                            bmi=row['bmi_code'],
                            gender=row['gender'],
                            year=row['year'],
                            crude_estimate=row['crude_estimate']
                        )
                        
                    else:
                        if model_name == 'PB_AU_CONCERN': # model PB_AU_CONCERN
                            model_class.objects.create(
                                concern=row['concern'], 
                                gender=row['gender'],
                                age_group=row['age_group'],
                                percentage=row['percentage']
                            )
                        else:  # model PB_AU_VEGGIE
                            model_class.objects.create( 
                                year=row['year'],			
                                concern=row['concern'],
                                concern_label=row['concern_label'],  
                                gender=row['gender'],
                                age_group=row['age_group'],
                                percentage=row['proportion'],
                                margin_error = row['95% Margin of Error of proportion']
                            )   
                    
                return HttpResponse(f"Data {file_name} has been stored in the {model_name} table.")
            else:
                return HttpResponse(f"Model {model_name} not found.")
        except FileNotFoundError:
            return HttpResponse(f"File {file_name} not found.")
    
    
#overweight info page    
class VeggiView(generic.TemplateView):
    template_name = 'CoreApp/vegetable.html'
    
    
   
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        super().get_context_data(**kwargs)

         # query from table
        all_data = PB_AU_VEGGIE.objects.all()
        serialized_data = serializers.serialize('json', all_data)
       
        # Convert the serialized data to a list of dictionaries
        data_list = json.loads(serialized_data)

        # Replace NaN with None
        for data in data_list:
            for key, value in data['fields'].items():
                if isinstance(value, float) and value != value:  # Check if value is NaN
                    data['fields'][key] = 0

        # Convert the data list back to JSON
        fixed_serialized_data = json.dumps(data_list)
        
        new_context = {'main_title': 'Veggie Insights',
                    #    'sub_title': 'Obesity and Overweight among Children',
                       'page_name': 'Veggie Insights',
                       'json_data': fixed_serialized_data,
                    #    'json_data_bmi': serialized_data_bmi
                       }
        
        return new_context


class LoadRecipesDataView(generic.View):
    def get(self, request, *args, **kwargs):
        
        
        # Files are stored in a folder named 'Data Sources' within your Django project directory
        file_address = os.path.join('Data Sources', 'recipes_list.json')
        
        try:
            with open(file_address, 'r') as f:
                # JSON to dictionary
                recipes = json.load(f)
                
                for r in recipes:
                    # TAG
                    for tag in r["recipe"]["healthLabels"]:
                        HEALTH_TAG.objects.create(tag=tag)
                    
                    # TYPE   
                    for type in r["recipe"]["mealType"]:
                        MEAL_TYPE.objects.create(type=type)
                    
                    # RECIPE
                    temp_recipe, created = RECIPES.objects.get_or_create(
                                                    name=r["recipe"]["label"],
                                                    description= r["recipe"]["url"]
                                                )
                    print(temp_recipe, created)
                    if created:
                        health_tags = HEALTH_TAG.objects.filter(tag__in=r["recipe"]["healthLabels"])
                        temp_recipe.health_tag.add(*health_tags)
                        
                        meals = MEAL_TYPE.objects.filter(type__in=r["recipe"]["mealType"])
                        temp_recipe.meal.add(*meals)
                    
                        
            return HttpResponse(f"Recipes are stored!")
                
        except FileNotFoundError:
            return HttpResponse(f"File recipes_list.json not found.")