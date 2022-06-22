from django import forms
from accounts.models import Doctors, CustomUser


class DoctorRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "First name"
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Last name"
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Username"
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Email"
    }))

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password"
    }))

    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Confirm password"
    }))

    class Meta:
        model = Doctors
        fields = ['first_name', 'last_name', 'username', 'gender', 'specialized_in', "email", "password1", "password2"]

        widgets = {
            'gender': forms.Select(choices=Doctors.gender_options, attrs={
                'class': 'form-control',
            }),
            'specialized_in': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def clean(self):
        cleaned_date = super().clean()
        username = cleaned_date.get("username")
        email = cleaned_date.get("email")
        password1 = cleaned_date.get("password1")
        password2 = cleaned_date.get("password2")
        if CustomUser.objects.filter(username=username).exists():
            self.add_error("username", "already taken")

        if CustomUser.objects.filter(email=email).exists():
            self.add_error("email", "already taken")

        if password2 != password1:
            self.add_error("password2", "The two password fields are mismatch..!")

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


class PatientRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "First name"
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Last name"
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Username"
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Email"
    }))

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password"
    }))

    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Confirm password"
    }))

    class Meta:
        model = Doctors
        fields = ['first_name', 'last_name', 'username', 'gender', "email", "password1", "password2"]

        widgets = {
            'gender': forms.Select(choices=Doctors.gender_options, attrs={
                'class': 'form-control',
            })
        }

    def clean(self):
        cleaned_date = super().clean()
        username = cleaned_date.get("username")
        email = cleaned_date.get("email")
        password1 = cleaned_date.get("password1")
        password2 = cleaned_date.get("password2")
        if CustomUser.objects.filter(username=username).exists():
            self.add_error("username", "already taken")

        if CustomUser.objects.filter(email=email).exists():
            self.add_error("email", "already taken")

        if password2 != password1:
            self.add_error("password2", "The two password fields are mismatch..!")

        return cleaned_date
