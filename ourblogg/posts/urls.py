from django.urls import  path
from django.conf.urls.static import static

from ourblogg import settings
from . import views

urlpatterns = [
    path('', views.PostsHomePage.as_view(), name='home'),
    path('my_posts/', views.ShowMyPosts.as_view(), name='my_posts'),
    path('new_post/', views.CreateNewPost.as_view(), name='new_post'),
    path('post/<slug:slug>', views.SelectedPost.as_view(), name='selected_post'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)