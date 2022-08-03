from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import DoctorSerializer, SpecialitiesSerializer
from doctors.models import Doctors, Specialities


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'doctor':
            return True


class DoctorDetailsView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]
    serializer_class = DoctorSerializer

    def get(self, request, *args, **kwargs):
        try:
            obj = Doctors.objects.get(details=request.user)
            serializer = self.serializer_class(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            if 'Doctors matching query does not exist.' in e.args:
                return Response({'message': 'you have to create doctors details'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'message': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        # should have check the doctor already added their details or not
        # because of that here I'm using try except block
        try:
            if request.user.doctor:
                return Response({'message': 'you already created.!'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            if 'CustomUser has no doctor.' in e.args:
                flag = 1
                context = dict
                if request.data.get('specialized_in_id'):
                    flag = 0
                    context = {
                        'user': request.user,
                        'special': Specialities.objects.get(id=request.data.get('specialized_in_id'))
                    }
                serializer = DoctorSerializer(data=request.data, context=context)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    custom_errors = serializer.errors
                    if flag == 1:  # for adding 'specialized_in_id field if it is not added
                        custom_errors['specialized_in_id'] = ["This field is required."]
                    return Response(custom_errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'msg': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        obj = Doctors.objects.get(details=request.user)
        context = {}
        if request.data.get('specialized_in_id'):
            context = {'special': Specialities.objects.get(id=request.data.get('specialized_in_id'))}
        serializer = self.serializer_class(data=request.data, instance=obj, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class SpecialitiesView(GenericAPIView, ListModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = SpecialitiesSerializer
    queryset = Specialities.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
