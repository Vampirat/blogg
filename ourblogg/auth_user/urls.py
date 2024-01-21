from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views


urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('update-profile/', views.UpdateUserProfile.as_view(), name='update-profile'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]