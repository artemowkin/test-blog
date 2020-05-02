from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse_lazy

from .models import Post


class JsonableResponseMixin:

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if not self.request.is_ajax():
            return response
        else:
            return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        if 'text/html' in self.request.headers.get('Accept', '*/*'):
            form.instance.author = self.request.user
            return super().form_valid(form)
        else:
            response_data = {}
            title = self.request.POST.get('title')
            body = self.request.POST.get('body')
            author = self.request.user

            response_data['title'] = title
            response_data['body'] = body
            response_data['author'] = author.username

            Post.objects.create(
                title=title,
                body=body,
                author=author,
            )

            return JsonResponse(response_data)


class PostListView(ListView):
    model = Post
    template_name = 'pages/home.html'
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    template_name = 'pages/post_detail.html'


class PostCreateView(JsonableResponseMixin, CreateView):
    model = Post
    fields = ('title', 'body')
    template_name = 'pages/post_create.html'

    def dispatch(self, *args, **kwargs):
        print('IM HERE')
        return super().dispatch(*args, **kwargs)


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
