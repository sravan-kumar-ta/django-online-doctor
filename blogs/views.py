from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView

from blogs.forms import PostForm
from blogs.models import Posts


def blogs(request):
    posts = Posts.objects.all()
    if request.user.role == 'doctor':
        print("innner")
        return render(request, 'doctor/blogs/blogs.html', {'posts': posts})
    else:
        return render(request, 'patient/blogs/blogs.html', {'posts': posts})


class ArticleDetailView(DetailView):
    model = Posts
    pk_url_kwarg = 'blog_id'
    context_object_name = 'post'
    template_name = 'doctor/blogs/blog_detail.html'


class AddPostView(CreateView):
    model = Posts
    form_class = PostForm
    template_name = 'doctor/blogs/add_post.html'
    success_url = reverse_lazy('blog:blogs')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Your post added..!")
        return super().form_valid(form)

