from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.models import CustomUser
from blogs.models import Posts
from doctors.models import Doctors, Specialities
from patients.models import FamilyMembers, Appointments


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'get_full_name', 'role']
        read_only_fields = fields


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)
    likes = UserSerializer(many=True, required=False)

    class Meta:
        model = Posts
        fields = ('id', 'is_public', 'title', 'content', 'image', 'date', 'author', 'total_likes', 'likes')
        depth = 1

    def create(self, validated_data):
        user = self.context.get('user')
        validated_data['is_public'] = True
        return Posts.objects.create(**validated_data, author=user)


class CustomUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'full_name']
        fields += ['email', 'gender', 'role', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        del validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        else:
            user = CustomUser.objects.create_user(**validated_data)
            user.set_password(validated_data['password'])
            user.save()
            return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ('old_password', 'new_password')


class FamilyMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyMembers
        fields = ('id', 'relation', 'name', 'age')

    def create(self, validated_data):
        user = self.context.get('user')
        return FamilyMembers.objects.create(**validated_data, relation_with=user)


class AvailableTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        exclude = ('details', 'profile_image', 'specialized_in', 'charge', 'paypal_account')


class SpecialitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialities
        exclude = ('slug',)


class DoctorSerializerForAppointment(serializers.ModelSerializer):
    specialized_in = SpecialitiesSerializer()
    details = UserSerializer()

    class Meta:
        model = Doctors
        fields = ('id', 'profile_image', 'charge', 'details', 'specialized_in')


class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializerForAppointment(read_only=True)

    class Meta:
        model = Appointments
        fields = ('id', 'date', 'time', 'status', 'doctor', 'date_time_start', 'date_time_end')
        depth = 2
        extra_kwargs = {
            'date_time_start': {'write_only': True},
            'date_time_end': {'write_only': True},
        }

    def create(self, validated_data):
        patient = self.context.get('patient')
        doctor = self.context.get('doctor')
        return Appointments.objects.create(**validated_data, doctor=doctor, patient=patient)


class DoctorSerializer(serializers.ModelSerializer):
    specialized_in = SpecialitiesSerializer(read_only=True)
    details = UserSerializer(read_only=True)

    class Meta:
        model = Doctors
        fields = '__all__'

    def validate(self, attrs):
        charge = attrs.get('charge')
        if charge > 1500 or charge < 100:
            raise serializers.ValidationError({'charge': "charge should be < 1500 and > 100"})
        return attrs

    def update(self, instance, validated_data):
        if self.context.get('special'):
            special = self.context.get('special')
            instance.specialized_in = special
            instance.save()
        return super().update(instance=instance, validated_data=validated_data)

    def create(self, validated_data):
        user = self.context.get('user')
        special = self.context.get('special')
        return Doctors.objects.create(**validated_data, details=user, specialized_in=special)
