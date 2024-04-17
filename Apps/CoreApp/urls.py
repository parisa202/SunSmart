from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from . import views


app_name = 'CoreApp'


urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('iteration1/obesity-overweight-children/', views.US11View.as_view(), name='US11'),
    path('iteration1/profile/', views.ProfileView.as_view(), name='profile'),
    path('iteration1/profile-child/', views.ProfileChildView.as_view(), name='profile-child'),
    path('iteration1/food-additives/', views.US13View.as_view(), name='US13'),
    path('iteration1/nutrition-guideline/', views.US21View.as_view(), name='US21'),
    path('iteration1/US22/', views.US22View.as_view(), name='US22'),
    path('iteration1/tracker-reminder/', views.US23View.as_view(), name='US23'),
    path('iteration1/recipe-nutrition-analysis/', views.GuestTrackerView.as_view(), name='guest_tracker'),
    path('iteration1/about-us/', views.AboutUsView.as_view(), name='about'),
    path('iteration1/login/', views.Login_RegisterView.as_view(), name='login_or_register'),
    path('iteration1/logout/', views.LogoutView.as_view(), name='logout'),
    path('iteration1/dash/', views.US11DashboardView.as_view(), name='dash'),
    path('iteration1/profile-dashboard/', views.US121View.as_view(), name='US121'),
    path('coming-soon/', views.ComingView.as_view(), name='coming'),
    path('iteration2/macronutrients-children/', views.MacronutrientsView.as_view(), name='macronutrients'),
    path('iteration2/recipe/', views.RecipeView.as_view(), name='recipe'),
    
    # import data views
    path('data/', views.ImportDataView.as_view(), name='import_data'),
    # /data/?file_name=pb_who_bmi.csv&model_name=PB_WHO_BMI
]

