from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from blogs.forms import PostForm
from blogs.models import Posts


def blogs(request):
    posts = Posts.objects.filter(is_public=True)
    if request.user.role == 'doctor':
        return render(request, 'doctor/blogs/blogs.html', {'posts': posts})
    else:
        return render(request, 'patient/blogs/blogs.html', {'posts': posts})


class MyArticlesListView(ListView):
    model = Posts
    context_object_name = 'posts'
    template_name = 'doctor/blogs/my_blogs.html'

    def get_queryset(self):
        return Posts.objects.filter(author=self.request.user)


class ArticleDetailView(DetailView):
    model = Posts
    pk_url_kwarg = 'blog_id'
    context_object_name = 'post'
    template_name = 'doctor/blogs/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        liked = False
        post = get_object_or_404(Posts, id=self.kwargs['blog_id'])
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['liked'] = liked
        return context


class AddPostView(CreateView):
    model = Posts
    form_class = PostForm
    template_name = 'doctor/blogs/add_post.html'
    success_url = reverse_lazy('blog:my-articles')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Your post added..!")
        return super().form_valid(form)


class UpdatePostView(UpdateView):
    model = Posts
    form_class = PostForm
    template_name = 'doctor/blogs/update_post.html'
    success_url = reverse_lazy('blog:my-articles')

    def form_valid(self, form):
        messages.success(self.request, "Your post updated..!")
        return super().form_valid(form)


def post_like(request, blog_id):
    post = get_object_or_404(Posts, id=blog_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('blog:article-detail', blog_id)
