from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

from .forms import RegisterUserForm, ProfileUpdateForm
from django.contrib.auth.models import User


class RegisterUser(CreateView):

    form_class = RegisterUserForm
    template_name = 'auth_user/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('login')

class LoginUser(LoginView):
    
    form_class = AuthenticationForm
    template_name = 'auth_user/login.html'
    extra_context = {'title': 'Войти'}

    def get_success_url(self) -> str:
        return reverse_lazy('home')
    
class UpdateUserProfile(LoginRequiredMixin, UpdateView):

    model = User
    form_class = ProfileUpdateForm
    template_name = 'auth_user/update_profile.html'
    extra_context = {'title': 'Редактирование профиля' }

    def get_success_url(self) -> str:
        return reverse_lazy('update-profile')
    
    def get_object(self, queryset=None):
        return self.request.user