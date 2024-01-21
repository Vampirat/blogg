from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class RegisterUserForm(UserCreationForm):

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Введите пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']

        labels = {
            'email': 'e-mail'
        }
        widgets = {
            'email': forms.TextInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise ValidationError('Поле email является обязательным')
        elif get_user_model().objects.filter(email=email).exists():
            raise ValidationError('Такой email уже существует')
        return email

class ProfileUpdateForm(forms.ModelForm):

    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput())
    email = forms.CharField(disabled=True, label='e-mail', widget=forms.TextInput())
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']

        labels = {
            'email': 'e-mail'
        }
        widgets = {
            'email': forms.TextInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
        }