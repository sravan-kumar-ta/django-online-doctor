from django import forms
from blogs.models import Posts


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        exclude = ['date', 'author']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Article Title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your content here...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }
