from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views import generic
from django.urls import reverse_lazy

from .forms import LoginForm, CreateForm


# Create your views here.
class Login(LoginView):
  form_class = LoginForm
  template_name = 'accounts/login.html'


class Logout(LogoutView):
  template_name = 'accounts/logout_done.html'


class Signup(generic.edit.CreateView):
  template_name = "accounts/signup.html"
  form_class = CreateForm
  success_url = reverse_lazy("accounts:login")
