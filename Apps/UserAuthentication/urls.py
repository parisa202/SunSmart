# This file is mostly copied from allAuth in order to have some modification on views and url patterns
# The reason for similar url names is that in most of allAuth view functions, they are called (redirected to) with these names
from django.urls import path, re_path
from . import views
from importlib import import_module
from django.urls import include, path



# app_name = 'UserAthentication'


urlpatterns = [
    #path('signup/', views.SignUpView.as_view(), name='signup'),
    # path('login/', views.login, name='login'),

]


