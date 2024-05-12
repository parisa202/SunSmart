from typing import Any
from django.http.request import HttpRequest as HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views import generic
from django.core.mail import send_mail
from django.core.management.utils import get_random_secret_key
from django.utils.text import slugify
from .models import *
from django.apps import apps
import os
from .utils import api_request, login_required
import pandas as pd
from django.core import serializers
import json
from . import clustering
import requests
from openai import OpenAI
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
    
class BmiCalculatorView(generic.TemplateView):
    template_name = 'CoreApp/bmi_calculator.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        super().get_context_data(**kwargs)
        new_context = {'main_title': 'BMI Calculator',
                       'sub_title': '',
                       'page_name': 'BMI Calculator'
                       }
        
        return new_context

class RecipeDetailView(generic.DetailView):
    model = RECIPES
    template_name = 'CoreApp/recipe_detail.html'
    slug_field = 'slug'
    context_object_name = 'the_recipe'
    
    # # Access ingredients for a recipe
    # ingredients_for_recipe = RECIPES.ingredients.all()
    # for ingredient in ingredients_for_recipe:
    #     print(f"{ingredient.name}: {RECIPE_INGREDIENT.objects.get(recipe=RECIPES, ingredient=ingredient).quantity}")
    
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context = super().get_context_data(**kwargs)
            
            # find similar recipes
            
            similar_recipes = clustering.recommended_recipes(recipe_id=self.get_object().pk)
            recommendations = RECIPES.objects.filter(pk__in=similar_recipes)
                       
            context.update({'recommendations': recommendations})
            
            return context
            
    


class RecipeListView(generic.ListView):
    template_name = 'CoreApp/recipe_list.html'
    model = RECIPES
    context_object_name = 'all_recipes'
    all_selected_options = None
    # paginate_by  = 12
       
    def get_queryset(self):
        queryset = super().get_queryset().distinct()           
        self.all_selected_options = []
        
        # GET parameters from the request 
        health_tag = self.request.GET.getlist('health_tag')
        meal = self.request.GET.getlist('meal')
        ingredient = self.request.GET.getlist('ingredient')
        sortby = self.request.GET.get('sortby', 'no_selection')
        
        # Use for check mark the selected filters in template
        self.all_selected_options.extend(health_tag)
        self.all_selected_options.extend(meal)
        self.all_selected_options.extend(ingredient)
        self.all_selected_options.append(sortby)
        
        # Filter queryset based on parameters
        if not (health_tag=='' or health_tag==[] or health_tag==None):
            tempQuery = reduce(or_, (Q(health_tag__tag__exact=t) for t in health_tag))
            queryset = queryset.filter(tempQuery)
            
        if not (meal=='' or meal==[] or meal==None):
            tempQuery = reduce(or_, (Q(meal__type__exact=t) for t in meal))
            queryset = queryset.filter(tempQuery)
            
        if not (ingredient=='' or ingredient==[] or ingredient==None):
            tempQuery = reduce(or_, (Q(ingredients__name__icontains=t) for t in ingredient))
            queryset = queryset.filter(tempQuery)
        
        # order by must be the last if clause
        if (sortby=='' or sortby==None):
            queryset = queryset.order_by('-created_on')
        
        else:
            if sortby=='popularity':
                queryset = queryset.order_by('-page_view__views')                                     
            if sortby=='date':
                queryset = queryset.order_by('-created_on')

        
        self.queryset = queryset
        
        return queryset
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        # query from table
        all_recipes_count = self.queryset.count()
               
        context.update({'main_title': 'Healthy Recipes',
                       'page_name': 'Healthy Recipes',
                       'all_recipes_count' : all_recipes_count,
                       'selected_options': self.all_selected_options,
                       })
        
        return context
    

class OuterRecipeAnalysisView(generic.TemplateView):
    template_name = 'CoreApp/outer_recipe_analysis.html'
    headers = {
        "Content-Type": "application/json"
    }

    def post(self, request, **kwargs):
        custom_recipe = request.POST.get('custom_recipe')
        recipe_intake = 1
        serving = 1
        
        
        # Open AI API 
        # Set up OpenAI API
        client = OpenAI(
            api_key=settings.OPENAI_TOKEN
            )

        # Call the OpenAI API to extract ingredients and amounts
        openai_response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
            {"role": "system", "content": "You are a helpful, pattern-following assistant that can extract all the ingredients and their amount from the given recipes. Complete the measurements if they are given as abbreviation."+
             " Make the amounts into float number if they are fractional.If the measurement was missing, specify it yourself. Remove the percentages of ingredients purity."},
            {"role": "user", "content": f"Extract all the ingredients and their amounts from the following recipe with this format 'Amount measure Ingredient name\n':\n{custom_recipe}"},
            ],
            max_tokens=3000,
            temperature=0.2,
        )

        # Parse the response to extract ingredients and amounts
        gpt_output = openai_response.choices[0].message.content
        ingredients = {}
        for line in gpt_output.split('\n'):
            parts = line.split(',')
            if len(parts) == 3:
                ingredient = parts[0].strip()
                amount = parts[1].strip()
                measure = parts[2].strip()
                ingredients[ingredient] = (amount, measure)

        # cleanded_ingredients = 
        database_ingredients = INGREDIENT.objects.values_list('name', flat=True).distinct()
        print(database_ingredients)

        
            
        # send sign-in data to juniorjoy API
        api_url = 'https://juniorjoy.site/api/api/calcucalories'
        data = {
            "query": gpt_output,
            "intake": recipe_intake,
            "serving": serving
        }

        response = requests.get(api_url, headers=self.headers, json=data)
        recipe = {}
        
        if response.status_code == 200:
            # Append the calorie information to the recipe
            recipe['nutrient_info'] = {'success': 'calorie information received'}            
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
                
        

        
        self.context = self.get_context_data(**kwargs)
        self.context['api_data'] = recipe
        self.context['gpt_response'] = gpt_output
        self.context['custom_recipe'] = custom_recipe
        
        return render(request, self.template_name, context=self.context)
                 


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

#overweight info page    
class SugarView(generic.TemplateView):
    template_name = 'CoreApp/sugar.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        super().get_context_data(**kwargs)

         # query from table
        #all_data = PB_AU_VEGGIE.objects.all()
        #serialized_data = serializers.serialize('json', all_data)
       
        # Convert the serialized data to a list of dictionaries
        #data_list = json.loads(serialized_data)

        # Replace NaN with None
        # for data in data_list:
        #     for key, value in data['fields'].items():
        #         if isinstance(value, float) and value != value:  # Check if value is NaN
        #             data['fields'][key] = 0

        # Convert the data list back to JSON
        # fixed_serialized_data = json.dumps(data_list)
        
        new_context = {'main_title': 'Sugar Insights',
                    #    'sub_title': 'Obesity and Overweight among Children',
                       'page_name': 'Sugar Insights',
                    #    'json_data': fixed_serialized_data,
                   
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
                    # create RECIPE
                    temp_recipe, created = RECIPES.objects.get_or_create(
                                                    name=r["recipe"]["label"],
                                                    description= r["recipe"]["url"],
                                                    url= r["recipe"]["url"],
                                                    total_time = r["recipe"]["totalTime"],
                                                    serving = r["recipe"]["yield"]
                                                )
                    if created:
                        # HEALTH TAG
                        for tag in r["recipe"]["healthLabels"]:
                            temp_health_tag, c = HEALTH_TAG.objects.get_or_create(tag=tag)
                            # adding Healthe tags
                            temp_recipe.health_tag.add(temp_health_tag)
                        
                        # MEAL TYPE   
                        for type in r["recipe"]["mealType"]:
                            temp_meal_type, c = MEAL_TYPE.objects.get_or_create(type=type)
                            # adding meal type
                            temp_recipe.meal.add(temp_meal_type)
                    
                        # DIET LABEL   
                        for label in r["recipe"]["dietLabels"]:
                            temp_diet_label, c = DIET_LABEL.objects.get_or_create(label=label)
                            # adding diet label
                            temp_recipe.diet_label.add(temp_diet_label)
                                                             
                        # INGREDIENTS
                        for ingredient in r["recipe"]["ingredients"]:
                            temp_ingredient, c = INGREDIENT.objects.get_or_create(name=ingredient['food'], food_category=ingredient['foodCategory'])   
 
                            # creating RECIPE_INGREDIENT
                            RECIPE_INGREDIENT.objects.create(
                                                        recipe = temp_recipe,
                                                        ingredient = temp_ingredient,
                                                        quantity = ingredient['quantity'],
                                                        measure = ingredient['measure'],
                                                        ingredient_text = ingredient['text']
                                                    )

                        # NUTRIENTS   
                        for key, nutrient in r["recipe"]["totalNutrients"].items():
                            temp_nutrient, c = NUTRIENTS.objects.get_or_create(name=nutrient['label'])   
 
                            # creating RECIPE_NUTRIENT
                            RECIPE_NUTRIENTS.objects.create(
                                                        recipe = temp_recipe,
                                                        nutrient = temp_nutrient,
                                                        quantity = nutrient['quantity'],
                                                        measure = nutrient['unit']
                                                    )  
                        
                    temp_recipe.save()                         
                    
                        
            return HttpResponse(f"Recipes are stored!")
                
        except FileNotFoundError:
            return HttpResponse(f"File recipes_list.json not found.")
        
        
class ExtractDataView(generic.View):
    def get(self, request, *args, **kwargs):
        cleaned_data = clustering.clean_data()
        features = clustering.feature_engineering(cleaned_data)
        clustered_data = clustering.k_means_cluster(features)
        
        
        # Example usage
        similar_recipes = clustering.get_similar_recipes(clustered_data,recipe_id=43, top_n=4)
        print(similar_recipes)

        similar_recipes.append(43)
        # Filtering DataFrame based on recipe_ids
        filtered_df = cleaned_data[cleaned_data['recipe_id'].isin(similar_recipes)]

        # Extracting recipe names from the filtered DataFrame
        recipe_names = filtered_df['recipe_name'].unique()
        print(recipe_names)
        
        return HttpResponse("Information has been extracted")