from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy

from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'pages/home.html'
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    template_name = 'pages/post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('title', 'body')
    template_name = 'pages/post_create.html'
    raise_exception = True

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return HttpResponseRedirect(obj.get_absolute_url())


class PostUpdateView(UpdateView):
    model = Post
    fields = ('title', 'body')
    template_name = 'pages/post_update.html'

    def dispatch(self, *args, **kwargs):
        obj = self.get_object()
        if (obj.author.username == self.request.user.username or
                self.request.user.is_staff):
            return super().dispatch(*args, **kwargs)

        raise Http404


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'pages/post_delete.html'
    success_url = reverse_lazy('homepage')

    def dispatch(self, *args, **kwargs):
        obj = self.get_object()
        if (obj.author.username == self.request.user.username or
                self.request.user.is_staff):
            return super().dispatch(*args, **kwargs)

        raise Http404
