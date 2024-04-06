from typing import Any
from django.shortcuts import render
from django.views import generic
from django.core.mail import send_mail
from django.core.management.utils import get_random_secret_key
from .models import *
from django.apps import apps
import os
import pandas as pd
from django.core import serializers
import json

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


class LoginView(generic.TemplateView):
    template_name = 'CoreApp/login.html'
    
class ComingView(generic.TemplateView):
    template_name = 'CoreApp/coming_soon.html'


class ImportDataView(generic.View):
     template_name = ''
    # def get(self, request, *args, **kwargs):
    #     file_name = kwargs['file_name']
    #     model_name = kwargs['model_name']
        
    #     # grab the model class using its name
    #     model_class =  apps.get_model('CoreApp', model_name)
        
    #     # Files are stored in a folder named 'Data Sources' within your Django project directory
    #     file_address = os.path.join('Data Sources', file_name)
        
    #     try:
    #         df = pd.read_csv(file_address)
    #         if model_class:
    #             for index, row in df.iterrows():
                    
    #                 # model PB_WHO_BMI
    #                 if model_name == 'PB_WHO_BMI':
    #                     model_class.objects.create(
    #                         bmi=row['bmi_code'],
    #                         gender=row['gender'],
    #                         year=row['year'],
    #                         crude_estimate=row['crude_estimate']
    #                     )
                        
    #                 else: # model PB_AU_CONCERN
    #                     model_class.objects.create(
    #                         concern=row['concern'], 
    #                         gender=row['gender'],
    #                         age_group=row['age_group'],
    #                         percentage=row['percentage']
    #                     )
                    
    #             return HttpResponse(f"Data {file_name} has been stored in the {model_name} table.")
    #         else:
    #             return HttpResponse(f"Model {model_name} not found.")
    #     except FileNotFoundError:
    #         return HttpResponse(f"File {file_name} not found.")