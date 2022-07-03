from django import forms
from blogs.models import Posts


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        exclude = ['date', 'author', 'likes']

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
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

        labels = {
            'is_public': 'Want to post publicly?'
        }
