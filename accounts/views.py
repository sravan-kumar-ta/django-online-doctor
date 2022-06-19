from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, "home.html")


def doctors(request):
    return render(request, "doctors.html")


def profile(request):
    return render(request, "profile.html")
