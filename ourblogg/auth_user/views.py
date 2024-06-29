from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render

from django.urls import reverse_lazy

from .forms import RegisterUserForm, ProfileUpdateForm, ProfilePasswordChangeForm
from .models import Profile, SubscriptionModel
from actions.utils import create_action
from actions.models import Action

class RegisterUser(CreateView):
    
    form_class = RegisterUserForm
    template_name = 'auth_user/register.html'
    extra_context = {'title': 'Регистрация',}
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        self.object = form.save()
        create_action(self.object, 'только что создал новый аккаунт!')
        return super().form_valid(form)

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
    return render(request, 'auth_user/social_profile.html', {'title': user.username , 'user': user})

@login_required
def all_profiles_list(request):
    profiles = Profile.objects.filter(is_active=True)
    return render(request, 'auth_user/all_profiles.html', {'title': 'Пользователи', 'users': profiles})


@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = Profile.objects.get(id=user_id)
            if action == 'Подписаться':
                SubscriptionModel.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, 'подписался на', user)
            else:
                SubscriptionModel.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except Profile.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})

@login_required
def new_actions(request):
    actions = Action.objects.all()    #exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)

    if following_ids:
        user_follow_actions = actions.filter(user_id__in=following_ids)
        if user_follow_actions:
            actions = user_follow_actions.select_related('user')[:10].prefetch_related('target')[:10]
        else:
            actions = actions.select_related('user')[:10].prefetch_related('target')[:10]
    return render(request, 'auth_user/new_actions.html', {'title': 'Лента активности', 'actions': actions})