from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView

from accounts.forms import DoctorRegistrationForm, PatientRegistrationForm, LoginForm
from accounts.models import Doctors, CustomUser, Specialities


class HomeView(ListView):
    model = Specialities
    context_object_name = "specialities"
    template_name = 'home.html'


class DoctorRegistrationView(CreateView):
    model = Doctors
    form_class = DoctorRegistrationForm
    template_name = "auth/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        first_name = form.cleaned_data.pop("first_name")
        last_name = form.cleaned_data.pop("last_name")
        password2 = form.cleaned_data.pop("password2")
        username = form.cleaned_data.pop("username")
        email = form.cleaned_data.pop("email")
        user = CustomUser.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            password=password2,
            username=username,
            email=email,
            role="doctor"
        )
        user.save()
        form.instance.role = user
        return super().form_valid(form)


class PatientsRegistrationView(CreateView):
    model = Doctors
    form_class = PatientRegistrationForm
    template_name = "auth/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        first_name = form.cleaned_data.pop("first_name")
        last_name = form.cleaned_data.pop("last_name")
        password2 = form.cleaned_data.pop("password2")
        username = form.cleaned_data.pop("username")
        email = form.cleaned_data.pop("email")
        user = CustomUser.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            password=password2,
            username=username,
            email=email,
            role="patient"
        )
        user.save()
        form.instance.role = user
        return super().form_valid(form)


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
