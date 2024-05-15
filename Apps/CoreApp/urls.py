from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from .views import RecipeDetailView, RecipeListView
from . import views


app_name = 'CoreApp'


urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('obesity-overweight-children/', views.US11View.as_view(), name='US11'),
    path('food-additives/', views.US13View.as_view(), name='US13'),
    path('nutrition-guideline/', views.US21View.as_view(), name='US21'),
    path('tracker-reminder/', views.ReminderView.as_view(), name='US23'),
    path('recipe-nutrition-analysis/', views.GuestTrackerView.as_view(), name='guest_tracker'),
    path('about-us/', views.AboutUsView.as_view(), name='about'),
    path('dash/', views.US11DashboardView.as_view(), name='dash'),
    path('coming-soon/', views.ComingView.as_view(), name='coming'),
    path('macronutrients-children/', views.MacronutrientsView.as_view(), name='macronutrients'),
    path('micronutrients-children/', views.MicronutrientsView.as_view(), name='micronutrients'),
    path('bmi-calculator/', views.BmiCalculatorView.as_view(), name='bmi_calculator'),
    # path('recipe/', views.RecipeView.as_view(), name='recipe'),
    path('recipes/', views.RecipeListView.as_view(), name='recipes'),
    path("recipes/<slug:slug>/", RecipeDetailView.as_view(), name="recipe-detail"),
    path('veggie-insights/', views.VeggiView.as_view(), name='Veggi'),
    path('custom-recipe-analysis/', views.OuterRecipeAnalysisView.as_view(), name='outer_recipe_analysis'),
    path('sugar-insights/',  views.SugarView.as_view(), name='sugar_insights'),
    
    path('dietary-awareness/',  views.DietAwarenessView.as_view(), name='dietary_awareness'),
    
    # import data views
    #path('data/', views.ImportDataView.as_view(), name='import_data'),
    path('rr/', views.LoadRecipesDataView.as_view()),
    path('ee/', views.ExtractDataView.as_view()),
    # /data/?file_name=pb_who_bmi.csv&model_name=PB_WHO_BMI
    
    
]

