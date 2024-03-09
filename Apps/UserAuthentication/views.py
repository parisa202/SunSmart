from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from django.contrib.auth import login
from django.urls import reverse_lazy


class SignUpView(generic.CreateView):
    form_class = forms.RegisterForm
    success_url = reverse_lazy('CoreApp:index')
    template_name = 'UserAuthentication/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)