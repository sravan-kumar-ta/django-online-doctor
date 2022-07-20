from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render

from patients.models import Appointments


# Create your views here.
def enter_room(request, app_id):
    appointment = Appointments.objects.get(id=app_id)

    date_format = '%Y-%m-%d-%H:%M:%S'
    start_time = datetime.strftime(appointment.date_time_start, date_format)
    end_time = datetime.strftime(appointment.date_time_end, date_format)
    new_date = datetime.strftime(datetime.now(), date_format)

    if start_time <= new_date <= end_time:
        doctor_details = appointment.doctor.details
        doctor = doctor_details.first_name + ' ' + doctor_details.last_name
        patient = appointment.patient.first_name + ' ' + appointment.patient.last_name
        room_name = str(app_id)
        context = {
            'doctor': doctor,
            'patient': patient,
            'room_name': room_name,
        }
        return render(request, 'chat/chat_room.html', context)
    return HttpResponse('You are trying to enter wrong chat room')
