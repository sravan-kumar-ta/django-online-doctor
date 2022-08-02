from datetime import datetime, timedelta

from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.serializers import FamilyMembersSerializer, AvailableTimeSerializer, AppointmentSerializer
from doctors.models import Doctors
from patients.models import FamilyMembers, Appointments
from patients.views import getStartEndTime, getAvailableTimes


class FamilyMemberViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FamilyMembersSerializer

    def get_queryset(self):
        return FamilyMembers.objects.filter(relation_with=self.request.user)

    def create(self, request, *args, **kwargs):
        if request.user.role == 'patient':
            serializer = self.get_serializer(data=request.data, context={'user': request.user})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({'message': 'Only patients can add family members.'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class AvailableDateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AvailableTimeSerializer

    def get(self, request, *args, **kwargs):
        doctor = Doctors.objects.get(id=kwargs['doc_id'])
        serializer = self.serializer_class(doctor)
        return Response(serializer.data)


class AvailableTimeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AvailableTimeSerializer

    def get(self, request, *args, **kwargs):
        doctor_id = kwargs.get('doc_id')
        date = kwargs['a_date']
        modified_date = datetime.strptime(date, "%Y-%m-%d").date()
        day = modified_date.isoweekday()
        duration = timedelta(minutes=30)

        # Appointments are taken according to the requested date and time
        appointments = Appointments.objects.filter(
            Q(doctor_id=doctor_id) & Q(date=modified_date) & (Q(status="upcoming") | Q(status="ongoing"))
        )

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

        available_times = {}
        if available_slots:
            for slot in available_slots:
                available_times[slot] = available_slots[slot].time()
        response = {
            'doctor_id': doctor_id,
            'date': modified_date,
            'slots': available_times
        }
        return Response({'Response': response})


class AppointmentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        return Appointments.objects.filter(patient=self.request.user)

    def create(self, request, *args, **kwargs):
        doc_id = request.data.get('doc_id')
        date = request.data.get('date')
        time = request.data.get('time')
        converted_date = datetime.strptime(date, "%Y-%m-%d").date()
        converted_time = datetime.strptime(time, "%H:%M:%S").time()
        new_date = datetime.combine(date=converted_date, time=converted_time)
        new_time = timezone.make_aware(new_date + timedelta(minutes=30))

        request_data = {
            'date': converted_date,
            'time': converted_time,
            'date_time_start': new_date,
            'date_time_end': new_time,
            'status': 'upcoming'
        }
        context = {
            'patient': request.user,
            'doctor': Doctors.objects.get(id=doc_id)
        }
        serializer = self.serializer_class(data=request_data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
