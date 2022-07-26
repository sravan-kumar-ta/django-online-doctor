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
            messages.success(self.request, 'Successfully logged in')
            return redirect('doctor:profile')
        elif user_data == "2" and user and user.role == "patient":
            login(self.request, user)
            return redirect('patient:home')
        else:
            messages.error(self.request, "Invalid credentials..!")
            return redirect('login')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Credentials')


def sign_out_view(request):
    logout(request)
    return redirect('patient:home')


def user_role_check(request):
    try:
        user = request.user
        if request.method == 'POST':
            user_data = request.POST.get("user")
            if user_data == '1':
                user.role = 'doctor'
                user.save()
                return redirect('doctor:profile')
            elif user_data == '2':
                user.role = 'patient'
                user.save()
                return redirect('patient:home')
            else:
                return redirect('logout')
        else:
            if user.role == 'admin':
                return render(request, 'account/select_role.html')
            elif user.role == 'doctor':
                return redirect('doctor:profile')
            elif user.role == 'patient':
                return redirect('patient:home')
            else:
                return redirect('logout')
    except:
        return redirect('logout')
