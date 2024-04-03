from typing import Any
from django.shortcuts import render
from django.views import generic
from django.core.mail import send_mail
from django.core.management.utils import get_random_secret_key
from .models import PB_AU_CONCERN
import pandas as pd

class HomeView(generic.TemplateView):
    template_name = 'CoreApp/index.html'
    
    def import_data(self):
        filename = "C:/Users/Parisa/Downloads/staging_pb_au_concern - pb_au_concern.csv"
        df = pd.read_csv(filename)
        for index, row in df.iterrows():
            temp_row = PB_AU_CONCERN(concern=row['concern'], 
                                        gender=row['gender'],
                                        age_group=row['age_group'],
                                        percentage=row['percentage'])
            
            temp_row.save()
        
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # import_data()

        return super().get_context_data(**kwargs)

    

class US11View(generic.TemplateView):
    template_name = 'CoreApp/us11.html'

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