from django.urls import path

from . import views
from .views import PostList, PostDetail, NewsCreate, ArticlesCreate, NewsUpdate, ArticlesUpdate, NewsDelete, \
   ArticlesDelete

urlpatterns = [
   path('', PostList.as_view()),
   path('posts/', views.PostList.as_view(), name='post_list'),
   path('posts/<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
   path('articles/<int:pk>/edit/', ArticlesUpdate.as_view(), name='articles_update'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
]
