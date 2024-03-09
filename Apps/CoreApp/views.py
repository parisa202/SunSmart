from django.shortcuts import render
from django.views import generic
from django.core.mail import send_mail
from django.core.management.utils import get_random_secret_key

class HomeView(generic.TemplateView):
    template_name = 'CoreApp/test.html'