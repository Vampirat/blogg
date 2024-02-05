from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured

from .models import PostsModel, CommentsModel
from .forms import NewPostForm, NewCommentsForm



class PostsHomePage(ListView):
    
    template_name = 'posts/index.html'
    queryset = PostsModel.objects.filter(is_published=True)
    paginate_by = 6
    extra_context = {
        'title': 'Главная стараница'
    }


class CreateNewPost(LoginRequiredMixin, CreateView):

    form_class = NewPostForm
    template_name = 'posts/new_post.html'
    extra_context = {'title': 'Новая Запись'}

    def form_valid(self, form):
        new_post = form.save(commit=False)
        new_post.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy('home')


class ShowMyPosts(LoginRequiredMixin, ListView):

    template_name = 'posts/my_posts.html'
    model = PostsModel
    extra_context = {
        'title': 'Мои записи'
    }
    
    def get_queryset(self):
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.model is not None:
            queryset = self.model._default_manager.filter(user=self.request.user)
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {"cls": self.__class__.__name__}
            )
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset
    

class SelectedPost(DetailView, CreateView):
    model = PostsModel
    template_name = 'posts/selected_post.html' 
    form_class = NewCommentsForm

    def form_valid(self, form):
        detail_post = PostsModel.objects.get(slug=self.kwargs['slug'])
        new_comment = form.save(commit=False)
        new_comment.user = self.request.user
        new_comment.post = detail_post
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('selected_post', kwargs={'slug':self.kwargs['slug']})


    