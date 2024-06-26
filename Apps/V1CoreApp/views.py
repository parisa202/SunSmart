from typing import Any
from django.http.request import HttpRequest as HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.core.mail import send_mail
from django.core.management.utils import get_random_secret_key
from .models import *
from django.apps import apps
import os
from .utils import api_request, login_required
import pandas as pd
from django.core import serializers
import json
import requests


class CustomLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if 'user_id' not in request.session:
            # Redirect to the login page
            messages.add_message(self.request, messages.INFO, 'You need to login to access the content')
            # Store the requested URL in the session
            request.session['next'] = request.get_full_path()
            return redirect('V1CoreApp:login_or_register')
        return super().dispatch(request, *args, **kwargs)
    
    
class HomeView(generic.TemplateView):
    template_name = 'V1CoreApp/index.html'
    
    def import_data(self):
        filename = "C:/Users/Parisa/Downloads/tb_concern.csv"
        df = pd.read_csv(filename)
        for index, row in df.iterrows():
            temp_row = PB_AU_CONCERN_V1(concern=row['concern'], 
                                        gender=row['gender'],
                                        age_group=row['age_group'],
                                        percentage=row['percentage'])
            
            temp_row.save()
    
    def import_bmi_data(self):
        filename = "C:/Users/Parisa/Downloads/pb_who_bmi.csv"
        df = pd.read_csv(filename)
        for index, row in df.iterrows():
            temp_row = PB_WHO_BMI_V1(bmi=row['bmi_code'], 
                                        gender=row['gender'],
                                        year=row['year'],
                                        crude_estimate=row['crude_estimate'])
            
            temp_row.save()
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        # self.import_bmi_data()
            
        return super().get_context_data(**kwargs)

#overweight info page    
class US11View(generic.TemplateView):
    template_name = 'V1CoreApp/us11.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        super().get_context_data(**kwargs)
        
        # query from table
        all_data = PB_AU_CONCERN_V1.objects.all()
        serialized_data = serializers.serialize('json', all_data)
        
        
        all_data_bmi = PB_WHO_BMI_V1.objects.all()
        serialized_data_bmi = serializers.serialize('json', all_data_bmi)
    
        
        new_context = {'main_title': 'Obesity and Overweight among Children',
                    #    'sub_title': 'Obesity and Overweight among Children',
                       'page_name': 'Obesity and Overweight',
                       'json_data': serialized_data,
                       'json_data_bmi': serialized_data_bmi}
        
        return new_context
        

class US11DashboardView(generic.TemplateView):
    template_name = 'V1CoreApp/us11_dashboard.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        super().get_context_data(**kwargs)
        
        # query from table
        all_data = PB_AU_CONCERN_V1.objects.all()
        serialized_data = serializers.serialize('json', all_data)
        
        
        all_data_bmi = PB_WHO_BMI_V1.objects.all()
        serialized_data_bmi = serializers.serialize('json', all_data_bmi)
    
        
        new_context = {'main_title': 'Checkout',
                       'sub_title': 'Shop',
                       'page_name': 'US11',
                       'json_data': serialized_data,
                       'json_data_bmi': serialized_data_bmi}
        
        return new_context


class ProfileView(CustomLoginRequiredMixin, generic.TemplateView):
    template_name = 'V1CoreApp/profile.html'
    recipes = None  
    
    def setup(self, request, *args, **kwargs):
        file_address = os.path.join('Data Sources', 'recipes.json')
        with open(file_address, 'r') as f:
            # JSON to dictionary
            self.recipes = json.load(f)
        return super().setup(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        new_context = {'main_title': 'Profile',
                    #    'sub_title': 'Obesity and Overweight among Children',
                       'page_name': 'Profile',
                       'recipes': self.recipes
                       }
        return new_context
    
    
class ProfileChildView(CustomLoginRequiredMixin, generic.TemplateView):
    template_name = 'V1CoreApp/profile_child.html'
    recipes = None  
    
    def setup(self, request, *args, **kwargs):
        file_address = os.path.join('Data Sources', 'recipes.json')
        with open(file_address, 'r') as f:
            # JSON to dictionary
            self.recipes = json.load(f)
        return super().setup(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        new_context = {'main_title': "Child's Profile",
                    #    'sub_title': 'Obesity and Overweight among Children',
                       'page_name': "Child's Profile",
                       'recipes': self.recipes
                       }
        return new_context
  
    
class US121View(generic.TemplateView):
    template_name = 'V1CoreApp/us121.html'


class US13View(generic.TemplateView):
    template_name = 'V1CoreApp/additive.html'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        super().get_context_data(**kwargs)
        
        
    
        
        new_context = {'main_title': 'Understanding Food Additives: Uses, Reactions, and Safety',
                       'sub_title': '',
                       'page_name': 'Understanding Food Additives'
                       }
        
        return new_context

#nutrition-guideline
class US21View(generic.TemplateView):
    template_name = 'V1CoreApp/nutrition-guideline.html'
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
    template_name = 'V1CoreApp/us22.html'

#Reminder page
class US23View(generic.TemplateView):
    template_name = 'V1CoreApp/reminder_main.html'
    def post(self, request):
        submit_data = request.POST.get('submit_data', None)
        messages.add_message(self.request, messages.SUCCESS, 'The information saved successfully')
        return redirect('V1CoreApp:US23')
        
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        super().get_context_data(**kwargs)
  
        new_context = {'main_title': 'Reminder',
                    #    'sub_title': 'Obesity and Overweight among Children',
                       'page_name': 'Reminder'
        }
        
        return new_context

class AboutUsView(generic.TemplateView):
    template_name = 'V1CoreApp/about_us.html'


# class GuestTrackerView(CustomLoginRequiredMixin, generic.TemplateView):
class GuestTrackerView(generic.TemplateView):
    template_name = 'V1CoreApp/Nutrition_Analysis.html'
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
            return redirect('V1CoreApp:guest_tracker')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        return {'recipes': self.recipes}  


#not complete
class Login_RegisterView(generic.TemplateView):
    template_name = 'V1CoreApp/login.html'
    
    def post(self, request, *args, **kwargs):
        
        form_type = request.POST.get('form_type')

        if form_type == 'signin':
        #     # Get the input value
        #     input_value = request.POST.get('signin-input')

        #     # Check if input is an email
        #     if re.match(self.EMAIL_REGEX, input_value):
        #         # send email sign-in data to email authentication API
        #         api_url = 'http://email-auth-api-url'
        #         data = {
        #             'email': input_value,
        #             'password': request.POST.get('signin-password')
        #         }
        #     # Check if input is a phone number
        #     elif re.match(self.PHONE_REGEX, input_value):
        #         # send phone sign-in data to phone authentication API
        #         api_url = 'http://phone-auth-api-url'
        #         data = {
        #             'phone': input_value,
        #             'password': request.POST.get('signin-password')
        #         }
        #     else:
        #         # Handle invalid input (neither email nor phone number)
        #         return HttpResponse('Invalid input')          
            
            
            
            
            
            # sign-in form data
            email = request.POST.get('singin-email')
            password = request.POST.get('singin-password')
            
            # send sign-in data to authentication API
            api_url = 'http://juniorjoy.site/api/auth/login'
            data = {
                'email': email,
                'password': password
            }
            response = api_request(url=api_url, parameters=data, request_type='POST')

            # handle response
            if response.status_code == 200:
                messages.add_message(self.request, messages.SUCCESS, 'User successfully logged in')
                request.session['user_id'] = 'user_id' # changed this text to actual user ID
                
                next_url = request.session.get('next')
                if next_url:
                    del request.session['next']  # Remove the stored URL from the session
                    return redirect(next_url)
                else:
                    return redirect('V1CoreApp:index')
            else: 
                messages.add_message(self.request, messages.WARNING, 'Something is wrong')
                request.session.pop('user_id', None) # removing the key from session
                return super().get(request, *args, **kwargs)

            
        elif form_type == 'register':
            # register form data
            email = request.POST.get('register-email')
            password = request.POST.get('register-password')
            
            # send register data to registration API
            api_url = 'http://juniorjoy.site/api/users'
            
            data = {
                'email': email,
                'password': password
            }
            
            response = api_request(url=api_url, parameters=data, request_type='POST')

            # handle response
            if response.status_code == 201:
                messages.add_message(self.request, messages.SUCCESS, 'User is created. Please log in')
                return redirect('V1CoreApp:login_or_register')
            else: 
                messages.add_message(self.request, messages.WARNING, 'Something is wrong')
                return super().get(request, *args, **kwargs)

        else:
            # Invalid form type
            return JsonResponse({'error': 'Invalid form type'}, status=400)
        


class LogoutView(generic.View):
    
    def get(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS, 'User logged out')
        request.session.pop('user_id', None) # removing the key from session
        
        return redirect('V1CoreApp:index')
    
    
class ComingView(generic.TemplateView):
    template_name = 'V1CoreApp/coming_soon.html'



class ImportDataView(generic.View):
    def get(self, request, *args, **kwargs):
        file_name = request.GET.get('file_name')
        model_name = request.GET.get('model_name')
        
        # grab the model class using its name
        model_class =  apps.get_model('V1CoreApp', model_name)
        
        # Files are stored in a folder named 'Data Sources' within your Django project directory
        file_address = os.path.join('Data Sources', file_name)
        
        try:
            df = pd.read_csv(file_address)
            if model_class:
                for index, row in df.iterrows():
                    
                    # model PB_WHO_BMI
                    if model_name == 'PB_WHO_BMI_V1':
                        model_class.objects.create(
                            bmi=row['bmi_code'],
                            gender=row['gender'],
                            year=row['year'],
                            crude_estimate=row['crude_estimate']
                        )
                        
                    else: # model PB_AU_CONCERN
                        model_class.objects.create(
                            concern=row['concern'], 
                            gender=row['gender'],
                            age_group=row['age_group'],
                            percentage=row['percentage']
                        )
                    
                return HttpResponse(f"Data {file_name} has been stored in the {model_name} table.")
            else:
                return HttpResponse(f"Model {model_name} not found.")
        except FileNotFoundError:
            return HttpResponse(f"File {file_name} not found.")
    
    

        