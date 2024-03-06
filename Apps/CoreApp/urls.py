from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'CoreApp'


urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),

]

