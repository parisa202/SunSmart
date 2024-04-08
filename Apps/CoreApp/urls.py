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
    path('guest_tracker/', views.GuestTrackerView.as_view(), name='guest_tracker'),
    path('about-us/', views.AboutUsView.as_view(), name='about'),
    path('login/', views.Login_RegisterView.as_view(), name='login_or_register'),
    path('dash/', views.US11DashboardView.as_view(), name='dash'),
    path('US121/', views.US121View.as_view(), name='US121'),
    path('coming-soon/', views.ComingView.as_view(), name='coming'),
    
    # import data views
    path('data/', views.ImportDataView.as_view(), name='import_data'),
    # /data/?file_name=pb_who_bmi.csv&model_name=PB_WHO_BMI
]

