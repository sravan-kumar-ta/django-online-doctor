from django.views.generic import CreateView

from doctors.forms import DoctorDetailsForm
from doctors.models import Specialities, Doctors


def specialised_categories(request):
    categories = Specialities.objects.all()
    form = DoctorDetailsForm()
    doctor = Doctors.objects.all()
    context = {
        'fm': form,
        'specialisations': categories,
        'doctors': doctor
    }
    return context
