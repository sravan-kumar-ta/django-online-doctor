from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from accounts.forms import CustomUserCreationForm, LoginForm
from accounts.models import CustomUser


class CustomUserCreationView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "account/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        role = self.request.POST.get("role")
        form.instance.role = role
        print(form.cleaned_data.get("password2"))
        print(form.cleaned_data.get("username"))
        return super().form_valid(form)


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'account/login.html'

    def form_valid(self, form):
        user_data = self.request.POST.get("user")
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user_data == "1" and user and user.role == "doctor":
            login(self.request, user)
            return redirect('doctor:profile')
        elif user_data == "2" and user and user.role == "patient":
            login(self.request, user)
            return redirect('patient:home')
        else:
            messages.error(self.request, "Invalid credentials..!")
            return redirect('login')


def sign_out_view(request):
    logout(request)
    return redirect('patient:home')


def user_role_check(request):
    user = request.user
    if request.method == 'POST':
        user_data = request.POST.get("user")
        if user_data == '1':
            user.role = 'doctor'
        elif user_data == '2':
            user.role = 'patient'
        else:
            return redirect('login')
        user.save()
        return redirect('patient:home')
    else:
        if user.role == 'admin':
            return render(request, 'account/select_role.html')
        else:
            return redirect('patient:home')
