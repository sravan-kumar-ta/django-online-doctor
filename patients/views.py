import time
from datetime import timedelta, datetime

import humanize
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView, UpdateView

from accounts.models import CustomUser
from doctors.models import Specialities, Doctors
from patients.models import Appointments
from patients.forms import PatientUpdateForm


class HomeView(ListView):
    model = Specialities
    context_object_name = "specialities"
    template_name = 'patient/home.html'


class DoctorsListView(ListView):
    model = Doctors
    context_object_name = 'doctors'
    template_name = 'patient/doctors.html'

    def get_queryset(self, **kwargs):
        doctors = super().get_queryset()
        specialised_slug = self.kwargs.get("s_slug")
        specialised_in = Specialities.objects.get(slug=specialised_slug)
        return doctors.filter(specialized_in=specialised_in)


class UserProfileView(TemplateView):
    template_name = 'patient/profile.html'


class UpdatePatientView(UpdateView):
    model = CustomUser
    pk_url_kwarg = 'p_id'
    form_class = PatientUpdateForm
    template_name = 'patient/update_patient.html'
    success_url = reverse_lazy('patient:profile')

    def get_success_url(self):
        messages.success(self.request, "Profile data updated successfully..!")
        return super().get_success_url()


def getStartEndTime(doctor, day, modified_date):
    time_start = None
    time_end = None
    if day == 1:
        time_start = doctor.mon_start
        time_end = doctor.mon_end
    elif day == 2:
        time_start = doctor.tue_start
        time_end = doctor.tue_end
    elif day == 3:
        time_start = doctor.wed_start
        time_end = doctor.wed_end
    elif day == 4:
        time_start = doctor.thu_start
        time_end = doctor.thu_end
    elif day == 5:
        time_start = doctor.fri_start
        time_end = doctor.fri_end
    elif day == 6:
        time_start = doctor.sat_start
        time_end = doctor.sat_end
    elif day == 7:
        time_start = doctor.sun_start
        time_end = doctor.sun_end
    try:
        return datetime.combine(modified_date, time_start), datetime.combine(modified_date, time_end)
    except:
        return None, None


def getAvailableTimes(booked_slots, duration, start_time, end_time):
    current = start_time
    count = 0
    available = {}
    while True:
        if current not in booked_slots:
            count += 1
            available[count] = current
        current += duration
        if current + duration > end_time:
            break
    return available


@csrf_exempt
def available_slot(request):
    time.sleep(2)
    doctor_id = request.POST.get('doctor_id')
    request_date = request.POST.get('date')
    modified_date = datetime.strptime(request_date, "%Y-%m-%d").date()
    day = modified_date.isoweekday()
    duration = timedelta(minutes=30)

    # Appointments are taken according to the requested date and time
    appointments = Appointments.objects.filter(Q(doctor_id=doctor_id) & Q(date=modified_date))

    doctor = Doctors.objects.get(pk=doctor_id)

    # take starting and ending time of day of the requested doctor
    start_time, end_time = getStartEndTime(doctor, day, modified_date)

    booked_slots = set()
    for appointment in appointments:
        booked_slots.add(
            datetime.combine(modified_date, appointment.time)
        )

    available_slots = {}
    if start_time:
        available_slots = getAvailableTimes(booked_slots, duration, start_time, end_time)
    response = {
        'success': 'success ' + doctor_id,
        'day': modified_date.isoweekday(),
        'gone': datetime.today().date() > modified_date,
        'slots': available_slots
    }
    return JsonResponse(response)


def create_appointment(request, d_id, app_date, start_time):
    # start_time 2:59 PM to be converted to 21:59:00
    in_time = datetime.strptime(start_time, "%I:%M %p")  # str to datetime.datetime (date+time) --> 1900-01-01 21:59:00
    out_time = datetime.strftime(in_time, "%H:%M:%S")  # datetime.datetime to str (time only) --> 21:59:00
    new_time = datetime.strptime(out_time, "%H:%M:%S").time()  # str to datetime.datetime (correct time) --> 21:59:00

    doctor = Doctors.objects.get(pk=d_id)
    patient = CustomUser.objects.get(pk=request.user.id)
    appointment_date = datetime.strptime(app_date, '%Y-%m-%d').date()
    modified_date = datetime.combine(date=appointment_date, time=new_time)
    app_end_time = timezone.make_aware(modified_date + timedelta(minutes=30))

    appointment = Appointments.objects.create(
        patient=patient,
        doctor=doctor,
        date=appointment_date,
        time=new_time,
        date_time_start=modified_date,
        date_time_end=app_end_time,
    )
    appointment.save()

    email_date = humanize.naturaldate(appointment_date)
    email_time = new_time.strftime("%I:%M %p")
    email_message = 'Hai ' + patient.first_name + ',\n\n\tYour appointment successfully scheduled with ' + \
                    'our ' + str(doctor.specialized_in) + ' doctor Dr.' + doctor.details.first_name + ' on ' + \
                    str(email_date) + ' at ' + str(email_time) + '.\n\nThank you...'
    mail_id = patient.email
    send_mail(
        'Appointment scheduled',
        email_message,
        'Online Doctor <your email id>',
        [mail_id],
        fail_silently=False,
    )

    messages.success(request, 'Your appointment has been scheduled...')
    return redirect('patient:home')


class AppointmentsListView(ListView):
    model = Appointments
    template_name = 'patient/appointments.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        currentTime = timezone.make_aware(datetime.now())
        appointments = Appointments.objects.filter(patient=self.request.user)
        app_complete = appointments.filter(Q(date_time_end__lt=currentTime))
        app_active = appointments.filter(Q(date_time_end__gte=currentTime) & Q(date_time_start__lte=currentTime))
        app_upcoming = appointments.filter(Q(date_time_start__gt=currentTime))
        context = {
            'app_complete': app_complete,
            'app_active': app_active,
            'app_upcoming': app_upcoming,
        }
        return context


def demo_appointment(request):
    patient = request.user
    doctor = Doctors.objects.get(id=11)
    today = datetime.today()
    appointment_date = today.date()
    appointment_time = today.time()
    appointment_time_start = datetime.combine(date=appointment_date, time=appointment_time)
    appointment_time_end = timezone.make_aware(appointment_time_start + timedelta(minutes=30))

    appointment = Appointments.objects.create(
        patient=patient,
        doctor=doctor,
        date=appointment_date,
        time=appointment_time,
        date_time_start=appointment_time_start,
        date_time_end=appointment_time_end,
    )
    appointment.save()

    email_date = humanize.naturaldate(appointment_date)
    email_time = appointment_time.strftime("%I:%M %p")
    email_message = 'Hai ' + patient.first_name + ',\n\n\tYour appointment successfully scheduled with ' + \
                    'our ' + str(doctor.specialized_in) + ' doctor Dr.' + doctor.details.first_name + ' on ' + \
                    str(email_date) + ' at ' + str(email_time) + '.\n\nThank you...'
    mail_id = patient.email
    send_mail(
        'Appointment scheduled',
        email_message,
        'Online Doctor <your email id>',
        [mail_id],
        fail_silently=False,
    )

    return redirect('patient:appointments')
