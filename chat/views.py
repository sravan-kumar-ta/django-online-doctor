from django.shortcuts import render

from patients.models import Appointments


# Create your views here.
def enter_room(request, app_id):
    appointment = Appointments.objects.get(id=app_id)
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
