from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView, UpdateView

from accounts.forms import CustomUserCreationForm, LoginForm, SpecialisedDoctorForm
from accounts.models import CustomUser, Specialities


class HomeView(ListView):
    model = Specialities
    context_object_name = "specialities"
    template_name = 'home.html'


class CustomUserCreationView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "auth/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        role = self.request.POST.get("role")
        form.instance.role = role
        return super().form_valid(form)


def add_doctor_specialisation(request, d_id):
    specialised_in_id = request.POST.get("specialisation")
    specialised_in = Specialities.objects.get(id=specialised_in_id)
    doctor = CustomUser.objects.get(id=d_id)
    doctor.specialized_in = specialised_in
    doctor.save()
    return redirect('home')


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'auth/login.html'

    def form_valid(self, form):
        user_data = self.request.POST.get("user")
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user_data == "1" and user and user.role == "doctor":
            login(self.request, user)
            return redirect('home')
        elif user_data == "2" and user and user.role == "patient":
            login(self.request, user)
            return redirect('home')
        else:
            messages.error(self.request, "Invalid credentials..!")
            return redirect('login')


def sign_out_view(request):
    logout(request)
    return redirect('home')


def doctors(request):
    return render(request, "doctors.html")


def profile(request):
    return render(request, "profile.html")
