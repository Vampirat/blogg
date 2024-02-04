from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError




class RegisterUserForm(UserCreationForm):

    username = forms.CharField(label='Логин', widget=forms.TextInput())
    password1 = forms.CharField(label='Введите пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput())
    photo = forms.ImageField(label='Photo')

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'photo']

        labels = {
            'email': 'e-mail'
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
        fields = ['username', 'email', 'first_name', 'last_name', 'photo']

        labels = {
            'email': 'e-mail'
        }
