from typing import Any
from django.http.request import HttpRequest as HttpRequest
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.core.mail import send_mail
from django.core.management.utils import get_random_secret_key
from .models import *
from django.apps import apps
import os
from .utils import api_request
import pandas as pd
from django.core import serializers
import json
import requests


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

    
class US11View(generic.TemplateView):
    template_name = 'CoreApp/us11.html'
    
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


class US12View(generic.TemplateView):
    template_name = 'CoreApp/us12.html'
 
    
class US121View(generic.TemplateView):
    template_name = 'CoreApp/us121.html'


class US13View(generic.TemplateView):
    template_name = 'CoreApp/us13.html'


class US21View(generic.TemplateView):
    template_name = 'CoreApp/us21.html'
    
    
class US22View(generic.TemplateView):
    template_name = 'CoreApp/us22.html'


class US23View(generic.TemplateView):
    template_name = 'CoreApp/us23.html'


class AboutUsView(generic.TemplateView):
    template_name = 'CoreApp/about_us.html'

class GuestTrackerView(generic.TemplateView):
    template_name = 'CoreApp/Guest_Tracker.html'
    recipes = None
    
    def setup(self, request, *args, **kwargs):
        file_address = os.path.join('Data Sources', 'recipes.json')
        with open(file_address, 'r') as f:
            # JSON to dictionary
            self.recipes = json.load(f)
            
        return super().setup(request, *args, **kwargs)
    
    def post(self, request):
        selected_recipe = request.POST.get('selected_recipe')
                        
        # if the post requst comes from AJAX call
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':       
            # find the recipe if recipes
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
                "intake": "1",
                "serving": recipe['recipe_servings']
            }
            
            # data = {
            #         "query":"3 tb Butter or margarineine",
            #         "intake" : 2,
            #         "serving" : 6
            #         }

            response = requests.get(api_url, params=data)
            headers = {
                        "Content-Type": "application/json"
                    }

            response = requests.get(api_url, headers=headers, json=data)
                
            print(response.json(), response.json())    
                
            return JsonResponse(recipe)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        return {'recipes': self.recipes}  


class Login_RegisterView(generic.TemplateView):
    template_name = 'CoreApp/login.html'
    
    def post(self, request):
        form_type = request.POST.get('form_type')

        if form_type == 'signin':
            # Get the input value
            input_value = request.POST.get('signin-input')

            # Check if input is an email
            if re.match(self.EMAIL_REGEX, input_value):
                # send email sign-in data to email authentication API
                api_url = 'http://email-auth-api-url'
                data = {
                    'email': input_value,
                    'password': request.POST.get('signin-password')
                }
            # Check if input is a phone number
            elif re.match(self.PHONE_REGEX, input_value):
                # send phone sign-in data to phone authentication API
                api_url = 'http://phone-auth-api-url'
                data = {
                    'phone': input_value,
                    'password': request.POST.get('signin-password')
                }
            else:
                # Handle invalid input (neither email nor phone number)
                return HttpResponse('Invalid input')          
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            # sign-in form data
            email = request.POST.get('singin-email')
            password = request.POST.get('singin-password')
            
            # send sign-in data to authentication API
            api_url = 'http://3.25.234.118:8081/api/auth/login'
            data = {
                'email': email,
                'password': password
            }
            
            # response = api_request(api_url, parameters=data, 'POST')
            
            # handle response
            # if response.status_code == 200:
            #     # messages.success(self.request, 'Profile Updated Successfully')
            #     return redirect('CoreApp:index')
            # else: 
            #     # messages.error(self.request, 'Something Wrong')
            #     return super().get(request, *args, **kwargs)

            
        elif form_type == 'register':
            # register form data
            username = request.POST.get('register-username')
            email = request.POST.get('register-email')
            password = request.POST.get('register-password')
            
            # send register data to registration API
            api_url = 'http://3.25.234.118:8081/api/users'
            
            data = {
                'username': username,
                'email': email,
                'password': password
            }
            
            # response = api_request(api_url, parameters=data, 'POST')

            # handle response
            # if response.status_code == 200:
            #     # messages.success(self.request, 'Profile Updated Successfully')
            #     return redirect('CoreApp:index')
            # else: 
            #     # messages.error(self.request, 'Something Wrong')
            #     return super().get(request, *args, **kwargs)

        else:
            # Invalid form type
            return JsonResponse({'error': 'Invalid form type'}, status=400)


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
    
    
    