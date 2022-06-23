from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomUser, Specialities


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password",
    }))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Confirm Password",
    }))

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'password1', 'password2']

        labels = {
            'email': _('Email'),
        }

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'gender': forms.Select(choices=CustomUser.gender_options, attrs={
                'class': 'form-control',
            }),
            'password1': forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Password"
            }),
            'password2': forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Confirm password"
            })
        }

    def clean(self):
        cleaned_date = super().clean()
        username = cleaned_date.get("username")
        email = cleaned_date.get("email")
        if CustomUser.objects.filter(username=username).exists():
            self.add_error("username", "already taken")

        if CustomUser.objects.filter(email=email).exists():
            self.add_error("email", "already taken")
        return cleaned_date


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Username"
    }))

    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password"
    }))


class SpecialisedDoctorForm(forms.ModelForm):
    specialized_in = forms.ChoiceField(choices=Specialities.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = CustomUser
        fields = ['specialized_in']
