import pytz
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import OuterRef, Exists
from django.http import HttpResponse

from django.urls import reverse_lazy
from django.views import View

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.shortcuts import redirect, render
from .filters import PostFilter
from .forms import PostForm
from .models import *
from .translation import PostTranslate
from datetime import datetime



class PostList(ListView):
    model = Post
    ordering = 'dataPost'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect(self.request.path)


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class NewsCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = 'news.add_post'


    def form_valid(self, form):
        form.instance.choicePost = 'NW'
        return super().form_valid(form)


class ArticlesCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'
    permission_required = 'news.add_post'


    def form_valid(self, form):
        form.instance.choicePost = 'AR'
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = 'news.change_post'


class ArticlesUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'
    permission_required = 'news.change_post'


class NewsDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = 'news.delete_post'


class ArticlesDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = 'news.delete_post'




def subscriptions(request, categories=None):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    posts_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                post=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'posts': posts_with_subscriptions},
    )


class Index(View):
    def get(self, request):
        models = PostTranslate

        context = {
            'models': models,
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones #  добавляем в контекст все доступные часовые пояса
        }

        return HttpResponse(render(request, 'translation.html', context))


    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')