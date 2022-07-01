from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView

from accounts.models import CustomUser
from doctors.forms import DoctorDetailsForm
from doctors.models import Doctors, Specialities
from patients.forms import PatientUpdateForm
from patients.models import Appointments


def add_doctor_details(request):
    if request.method == 'POST':
        form = DoctorDetailsForm(request.POST)
        if form.is_valid():
            form.instance.details = request.user
            form.save()
    return redirect('doctor:profile')


class UpdatePatientView(UpdateView):
    model = CustomUser
    pk_url_kwarg = 'p_id'
    form_class = PatientUpdateForm
    template_name = 'patient/update_patient.html'
    success_url = reverse_lazy('doctor:profile')

    def get_success_url(self):
        messages.success(self.request, "Profile data updated successfully..!")
        return super().get_success_url()


def profile(request):
    doctor = Doctors.objects.get(details_id=request.user.id)
    specialities = Specialities.objects.all()
    context = {
        'doctor': doctor,
        'specialities': specialities
    }
    return render(request, 'doctor/profile.html', context)


def update_details(request):
    special_id = request.POST.get('special')
    charge = request.POST.get('charge')
    special = Specialities.objects.get(id=special_id)

    doctor = Doctors.objects.get(details_id=request.user.id)
    doctor.specialized_in = special
    doctor.charge = charge
    doctor.save()
    return redirect('doctor:profile')


class AppointmentsView(ListView):
    model = Appointments
    context_object_name = 'appointments'
    template_name = 'doctor/appointments.html'

    def get_queryset(self):
        return self.model.objects.filter(doctor=self.request.user).order_by('-date_time_start')
