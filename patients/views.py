import time
from datetime import timedelta, datetime

from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView, UpdateView

from accounts.models import CustomUser
from doctors.models import Specialities, Doctors
from patients.models import FamilyMembers, Appointments
from patients.forms import UpdateMemberForm, PatientUpdateForm


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


def add_family_member_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        relation = request.POST.get('relation')
        age = request.POST.get('age')

        member = FamilyMembers.objects.create(
            relation_with=request.user,
            relation=relation,
            name=name,
            age=age,
        )
        member.save()
        messages.success(request, "Successfully added new member..!")
        return redirect('patient:profile')


class UserProfileView(TemplateView):
    template_name = 'patient/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = FamilyMembers.objects.filter(relation_with=self.request.user.id)
        return context


class UpdateMemberView(UpdateView):
    model = FamilyMembers
    pk_url_kwarg = 'm_id'
    context_object_name = 'member'
    form_class = UpdateMemberForm
    template_name = 'patient/update_member.html'
    success_url = reverse_lazy('patient:profile')

    def get_success_url(self):
        messages.success(self.request, "Family member updated successfully..!")
        return super().get_success_url()


class UpdatePatientView(UpdateView):
    model = CustomUser
    pk_url_kwarg = 'p_id'
    form_class = PatientUpdateForm
    template_name = 'patient/update_patient.html'
    success_url = reverse_lazy('patient:profile')

    def get_success_url(self):
        messages.success(self.request, "Profile data updated successfully..!")
        return super().get_success_url()


def delete_member(request, m_id):
    member = FamilyMembers.objects.get(id=m_id)
    member.delete()
    messages.success(request, "Deleted successfully..")
    return redirect('patient:profile')


def getStartEndTime(doctor, day):
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
        return time_start, time_end
    except:
        return None, None


def getAvailableTimes(date, booked_slots, start_time, end_time):
    current = datetime.combine(date, start_time)
    end_time = datetime.combine(date, end_time)
    duration = timedelta(minutes=30)
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

    # Appointments are taken according to the requested date and time
    appointments = Appointments.objects.filter(
        Q(doctor_id=doctor_id) & Q(date=modified_date) & (Q(status="upcoming") | Q(status="ongoing"))
    )
    doctor = CustomUser.objects.get(pk=doctor_id).doctor

    # take starting and ending time of day of the requested doctor
    start_time, end_time = getStartEndTime(doctor, day)

    booked_slots = set()
    for appointment in appointments:
        booked_slots.add(appointment.time)

    available_slots = {}
    if start_time:
        available_slots = getAvailableTimes(modified_date, booked_slots, start_time, end_time)
    response = {
        'success': 'success ' + doctor_id,
        'day': modified_date.isoweekday(),
        'gone': datetime.today().date() > modified_date,
        'slots': available_slots
    }
    return JsonResponse(response)


def create_appointment(request, d_id, app_date, start_time):
    doctor = CustomUser.objects.get(pk=d_id)
    patient = CustomUser.objects.get(pk=request.user.id)
    appointment_date = datetime.strptime(app_date, '%Y-%m-%d').date()
    appointment_time = datetime.strptime(start_time, "%I:%M %p").time()
    new_date = datetime.combine(date=appointment_date, time=appointment_time)
    app_end_time = timezone.make_aware(new_date + timedelta(minutes=30))

    appointment = Appointments.objects.create(
        patient=patient,
        doctor=doctor,
        date=appointment_date,
        time=appointment_time,
        date_time_start=new_date,
        date_time_end=app_end_time,
        status='upcoming'
    )
    appointment.save()

    return redirect('patient:home')
