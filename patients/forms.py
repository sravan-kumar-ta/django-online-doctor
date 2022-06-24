from django import forms

from accounts.models import CustomUser
from patients.models import FamilyMembers


class PatientUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'gender',
        ]

        labels = {
            'email': 'Email'
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


class UpdateMemberForm(forms.ModelForm):
    class Meta:
        model = FamilyMembers
        exclude = ('relation_with', 'relation')

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control'
            })
        }
