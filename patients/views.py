from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, UpdateView

from accounts.models import CustomUser
from doctors.models import Specialities, Doctors
from patients.models import FamilyMembers
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
