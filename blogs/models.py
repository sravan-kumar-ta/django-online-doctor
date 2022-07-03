from django.db import models

from accounts.models import CustomUser


class Posts(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='images/blogs', null=True)
    is_public = models.BooleanField(default=True)
    likes = models.ManyToManyField(CustomUser, related_name='blog_post')

    def __str__(self):
        return self.title + ' | ' + self.author.first_name

    def total_likes(self):
        return self.likes.count()
