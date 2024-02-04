from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured

from .models import PostsModel
from .forms import NewPostForm



class PostsHomePage(ListView):
    
    template_name = 'posts/index.html'
    queryset = PostsModel.objects.filter(is_published=True)
    paginate_by = 6


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
    

class SelectedPost(DetailView):
    model = PostsModel
    template_name = 'posts/selected_post.html'