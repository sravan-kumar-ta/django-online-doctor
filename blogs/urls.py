from django.urls import path
from blogs import views

app_name = 'blog'


urlpatterns = [
    path('', views.blogs, name='blogs'),
    path('my_articles/', views.MyArticlesListView.as_view(), name='my-articles'),
    path('article/<int:blog_id>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('add-post/', views.AddPostView.as_view(), name='add-article'),
    path('update-post/<int:pk>/', views.UpdatePostView.as_view(), name='update-article'),
    path('like-post/<int:blog_id>/', views.post_like, name='like-article'),
]
