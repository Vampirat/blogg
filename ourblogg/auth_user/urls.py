from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('update-profile/', views.UpdateUserProfile.as_view(), name='update_profile'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/<username>/', views.social_profile, name='social_profile'),
    path('profiles/', views.all_profiles_list, name='all_profiles'),
    
    #cмена пароля
    path('password-change/', views.ProfilePasswordChange.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='auth_user/password_change_done.html'), name='password_change_done'),
    

    #сброс пароля
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='auth_user/password_reset_form.html'), 
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='auth_user/password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth_user/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='auth_user/password_reset_complete.html'), 
         name='password_reset_complete')
]

