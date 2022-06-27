from django.shortcuts import render, redirect
from doctors.forms import DoctorDetailsForm


# Create your views here.
def profile(request):
    return render(request, 'doctor/profile.html')


def add_doctor_details(request):
    if request.method == 'POST':
        form = DoctorDetailsForm(request.POST)
        if form.is_valid():
            form.instance.details = request.user
            form.save()
    return redirect('patient:home')
