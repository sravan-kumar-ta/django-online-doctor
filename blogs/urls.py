from django.urls import path
from blogs import views

app_name = 'blog'


urlpatterns = [
    path('', views.blogs, name='blogs'),
    path('article/<int:blog_id>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('add-post/', views.AddPostView.as_view(), name='add-article'),
]
