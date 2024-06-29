from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import PostsModel
from .forms import NewPostForm, NewCommentsForm

from .utils import get_hashtag
from actions.utils import create_action

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
        tags_list = get_hashtag(form.cleaned_data['text'])
        new_post = form.save(commit=False)
        new_post.user = self.request.user
        new_post.save()
        create_action(self.request.user, 'запостил', new_post)
        for tag in tags_list:
            new_post.tags.add(tag)
        new_post.save()
        form.save_m2m()
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy('home')


class ShowMyPosts(LoginRequiredMixin, ListView):

    template_name = 'posts/my_posts.html'
    model = PostsModel
    paginate_by = 6
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
        create_action(self.request.user, 'оставил комментарий к', detail_post)
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('selected_post', kwargs={'slug':self.kwargs['slug']})

class SelectedTags(ListView):

    template_name = 'posts/index.html'
    paginate_by = 6
    model = PostsModel
    extra_context = {
        'title': 'Поиск по hashtags'
    }
    
    def get_queryset(self):
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.model is not None:
            hashtag = self.kwargs['slug']
            find = PostsModel.tags.get(slug=hashtag)
            queryset = self.model._default_manager.filter(is_published=True, tags=find.pk)
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
    
@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = PostsModel.objects.get(id=post_id)
            if action == 'like':
                post.users_likes.add(request.user)
                create_action(request.user, 'лайкнул', post)
            else:
                post.users_likes.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except PostsModel.DoesNotExist:
            pass
        return JsonResponse({'status': 'error'})