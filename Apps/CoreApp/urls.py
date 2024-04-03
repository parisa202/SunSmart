from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'CoreApp'


urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('US11/', views.US11View.as_view(), name='US11'),
    path('US12/', views.US12View.as_view(), name='US12'),
    path('US13/', views.US13View.as_view(), name='US13'),
    path('US21/', views.US21View.as_view(), name='US21'),
    path('US22/', views.US22View.as_view(), name='US22'),
    path('US23/', views.US23View.as_view(), name='US23'),
    path('about-us/', views.AboutUsView.as_view(), name='about_us'),

]

