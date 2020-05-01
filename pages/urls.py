from django.urls import path

from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

urlpatterns = [
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/update/<int:pk>/', PostUpdateView.as_view(),
        name='post_update'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(),
        name='post_delete'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('', PostListView.as_view(), name='homepage'),
]
