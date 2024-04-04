from typing import Any
from django.shortcuts import render
from django.views import generic
from django.core.mail import send_mail
from django.core.management.utils import get_random_secret_key
from .models import PB_AU_CONCERN
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
        
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        # self.import_data()
            
        return super().get_context_data(**kwargs)

    

class US11View(generic.TemplateView):
    template_name = 'CoreApp/us11.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        super().get_context_data(**kwargs)
        
        # query from table
        all_data = PB_AU_CONCERN.objects.all()
        serialized_data = serializers.serialize('json', all_data, fields=["concern", "gender", "age_group", "percentage"])
        
        # Deserialize JSON
        deserialized_data = json.loads(serialized_data)

        # Modify each object to remove 'pk' and 'model' keys
        modified_data = []
        for obj in deserialized_data:
            modified_obj = {k: v for k, v in obj['fields'].items() if k != 'pk' or k != 'model'}
            modified_data.append(modified_obj)
        
        new_context = {'main_title': 'Checkout',
                       'sub_title': 'Shop',
                       'page_name': 'US11',
                       'all_data': all_data,
                       'json_data': modified_data}
        
        return new_context

class US11DashboardView(generic.TemplateView):
    template_name = 'CoreApp/us11_dashboard.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        super().get_context_data(**kwargs)
        
        # query from table
        all_data = PB_AU_CONCERN.objects.all()
        serialized_data = serializers.serialize('json', all_data, fields=["concern", "gender", "age_group", "percentage"])
        
        # Deserialize JSON
        deserialized_data = json.loads(serialized_data)

        # Modify each object to remove 'pk' and 'model' keys
        modified_data = []
        for obj in deserialized_data:
            modified_obj = {k: v for k, v in obj['fields'].items() if k != 'pk' or k != 'model'}
            modified_data.append(modified_obj)
        
        new_context = {'main_title': 'Checkout',
                       'sub_title': 'Shop',
                       'page_name': 'US11',
                       'all_data': all_data,
                       'json_data': serialized_data}
        
        return new_context


class US12View(generic.TemplateView):
    template_name = 'CoreApp/us12.html'

class US13View(generic.TemplateView):
    template_name = 'CoreApp/us13.html'

class US21View(generic.TemplateView):
    template_name = 'CoreApp/us21.html'
    
class US22View(generic.TemplateView):
    template_name = 'CoreApp/us22.html'

class US23View(generic.TemplateView):
    template_name = 'CoreApp/us23.html'

class AboutUsView(generic.TemplateView):
    template_name = 'CoreApp/about-us.html'

class LoginView(generic.TemplateView):
    template_name = 'CoreApp/login.html'