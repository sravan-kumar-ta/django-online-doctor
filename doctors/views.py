from datetime import datetime

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import UpdateView, ListView

from accounts.models import CustomUser
from doctors.forms import DoctorDetailsForm, AvailableTimeUpdationForm
from doctors.models import Doctors, Specialities
from patients.forms import PatientUpdateForm
from patients.models import Appointments


def add_doctor_details(request):
    print('function called')
    if request.method == 'POST':
        form = DoctorDetailsForm(request.POST)
        print('form opened')
        if form.is_valid():
            print('form valid')
            form.instance.details = request.user
            form.save()
            messages.success(request, 'Successfully added details')
    return redirect('doctor:profile')


class UpdatePatientView(UpdateView):
    model = CustomUser
    pk_url_kwarg = 'dtr_id'
    form_class = PatientUpdateForm
    template_name = 'doctor/update_doctor.html'
    success_url = reverse_lazy('doctor:profile')

    def get_success_url(self):
        messages.success(self.request, "Profile data updated successfully..!")
        return super().get_success_url()


def profile(request):
    try:
        doctor = Doctors.objects.get(details_id=request.user.id)
        form = AvailableTimeUpdationForm(instance=doctor)
    except:
        doctor = None
        form = AvailableTimeUpdationForm()
    context = {
        'doctor': doctor,
        'form': form
    }
    return render(request, 'doctor/profile.html', context)


def update_details(request):
    special_id = request.POST.get('special')
    charge = request.POST.get('charge')
    paypal = request.POST.get('paypal')
    special = Specialities.objects.get(id=special_id)

    doctor = Doctors.objects.get(details_id=request.user.id)
    doctor.specialized_in = special
    doctor.charge = charge
    doctor.paypal_account = paypal
    doctor.save()
    messages.success(request, "Your account details updated..")
    return redirect('doctor:profile')


def update_available_time(request, dtr_id):
    form = AvailableTimeUpdationForm(request.POST, instance=Doctors.objects.get(id=dtr_id))
    if form.is_valid():
        form.save()
        messages.success(request, "Available time updated..")
        return redirect('doctor:profile')
    return redirect('doctor:profile')


class AppointmentsView(ListView):
    model = Appointments
    context_object_name = 'appointments'
    template_name = 'doctor/appointments.html'

    def get_queryset(self):
        try:
            # before adding doctor details there have no doctor table, so we can't retrieve appointments
            # So before adding doctor details always run except block
            return self.model.objects.filter(doctor=self.request.user.doctor.id).order_by('-date_time_start')
        except:
            return None


def appointments_filter(request, filter):
    appointments = Appointments.objects.filter(doctor=request.user.doctor.id)
    currentTime = timezone.make_aware(datetime.now())
    if filter == 1:
        appointments = appointments.filter(Q(date_time_start__gt=currentTime))
    if filter == 2:
        appointments = appointments.filter(Q(date_time_end__gte=currentTime) & Q(date_time_start__lte=currentTime))
    if filter == 3:
        appointments = appointments.filter(Q(date_time_end__lt=currentTime))

    context = {
        'appointments': appointments,
        'filter': filter
    }

    return render(request, 'doctor/appointments.html', context)
