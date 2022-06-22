from accounts.models import Specialities


def specialised_categories(request):
    categories = Specialities.objects.all()
    return {'specialisations': categories}
