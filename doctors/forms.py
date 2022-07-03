from django import forms
from doctors.models import Doctors


class DoctorDetailsForm(forms.ModelForm):
    class Meta:
        model = Doctors
        exclude = ['details', 'profile_image']

        widgets = {
            'specialized_in': forms.Select(attrs={'class': 'form-control'}),
            'charge': forms.NumberInput(attrs={'class': 'form-control'}),
            'sun_start': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'sun_end': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'mon_start': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'mon_end': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'tue_start': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'tue_end': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'wed_start': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'wed_end': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'thu_start': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'thu_end': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'fri_start': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'fri_end': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'sat_start': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'sat_end': forms.TimeInput(attrs={'type': 'time', 'required': False}),
        }

    def clean(self):
        cleaned_data = super().clean()
        charge = cleaned_data.get('charge')
        if charge > 1500 or charge < 100:
            self.add_error('charge', "please give correct amount")

        return cleaned_data


class AvailableTimeUpdationForm(forms.ModelForm):
    class Meta:
        model = Doctors
        exclude = ['details', 'profile_image', 'specialized_in', 'charge']

        widgets = {
            'sun_start': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'sun_end': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'mon_start': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'mon_end': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'tue_start': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'tue_end': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'wed_start': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'wed_end': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'thu_start': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'thu_end': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'fri_start': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'fri_end': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'sat_start': forms.TimeInput(attrs={'type': 'time', 'required': False}),
            'sat_end': forms.TimeInput(attrs={'type': 'time', 'required': False}),
        }
