from django.shortcuts import render
from django.views.generic import ListView

from accounts.models import Specialities, CustomUser


class HomeView(ListView):
    model = Specialities
    context_object_name = "specialities"
    template_name = 'patient/home.html'


class DoctorsListView(ListView):
    model = CustomUser
    context_object_name = 'doctors'
    template_name = 'patient/doctors.html'

    def get_queryset(self, **kwargs):
        doctors = super().get_queryset()
        specialised_slug = self.kwargs.get("s_slug")
        special = Specialities.objects.get(slug=specialised_slug)
        return doctors.filter(specialized_in=special.id)


def doctors(request):
    return render(request, "patient/doctors.html")


def profile(request):
    return render(request, "patient/profile.html")
