from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .forms import RegisterUserForm, ProfileUpdateForm, ProfilePasswordChangeForm
from .models import Profile



class RegisterUser(CreateView):
    
    form_class = RegisterUserForm
    template_name = 'auth_user/register.html'
    extra_context = {'title': 'Регистрация',}
    success_url = reverse_lazy('login')

class LoginUser(LoginView):
    
    form_class = AuthenticationForm
    template_name = 'auth_user/login.html'
    extra_context = {'title': 'Войти'}

    
class UpdateUserProfile(LoginRequiredMixin, UpdateView):

    model = get_user_model()
    form_class = ProfileUpdateForm
    template_name = 'auth_user/update_profile.html'
    extra_context = {'title': 'Редактирование профиля', }

    def get_success_url(self) -> str:
        return reverse_lazy('update_profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    
class ProfilePasswordChange(PasswordChangeView):
    
    form_class = ProfilePasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'auth_user/password_change_form.html'
    title = ('Смена пароля')


@login_required
def social_profile(request, username):
    user = get_object_or_404(Profile, username=username, is_active=True)
    return render(request, 'auth_user/social_profile.html', {'user': user})

@login_required
def all_profiles_list(request):
    profiles = Profile.objects.filter(is_active=True)
    return render(request, 'auth_user/all_profiles.html', {'title': 'Пользователи', 'users': profiles})