from datetime import datetime, timedelta

from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission
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


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'patient':
            return True


class AppointmentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsPatient]
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        return Appointments.objects.filter(patient=self.request.user)

    def create(self, request, *args, **kwargs):
        doc_id = request.data.get('doc_id')
        date = request.data.get('date')
        time = request.data.get('time')
        if doc_id is None or date is None or time is None:
            return Response({
                "doc_id": ["This field is required."],
                "date": ["This field is required."],
                "time": ["This field is required."]
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        converted_date = datetime.strptime(date, "%Y-%m-%d").date()
        converted_time = datetime.strptime(time, "%H:%M:%S").time()
        date_time_start = datetime.combine(date=converted_date, time=converted_time)
        date_time_end = timezone.make_aware(date_time_start + timedelta(minutes=30))

        request_data = {
            'date': converted_date,
            'time': converted_time,
            'date_time_start': date_time_start,
            'date_time_end': date_time_end,
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

    def partial_update(self, request, *args, **kwargs):
        app_status = request.data.get('status') or None
        if app_status is None:
            return Response({"status": ["This field is required."]}, status=status.HTTP_406_NOT_ACCEPTABLE)
        request_data = {
            'status': app_status
        }  # just only update the status

        serializer = self.get_serializer(instance=self.get_object(), data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return Response({'message': 'This content is not updatable'}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'This content is not destroyable'}, status=status.HTTP_403_FORBIDDEN)
