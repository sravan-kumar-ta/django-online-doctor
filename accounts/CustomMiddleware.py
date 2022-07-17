from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

admin_permissions = [
    'django.views.static',
    'django.contrib.auth.views',
    'django.contrib.admin.sites',
    'django.contrib.admin.options',
]

doctor_permissions = [
    'django.views.static',
    'patients.views',
    'accounts.views',
]

patient_permissions = [
    'patients.views',
    'accounts.views',
]

anonymous_user_permission = [
    'allauth.account.views',
    'django.contrib.auth.views',
    'django.contrib.admin.sites',
    'accounts.views',
]


class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        module_name = view_func.__module__
        user = request.user
        if user.is_authenticated:
            if user.role == 'admin':
                if module_name in admin_permissions:
                    pass
                else:
                    return HttpResponseRedirect(reverse('logout'))
            elif user.role == 'doctor':
                if module_name in doctor_permissions:
                    pass
                else:
                    return HttpResponseRedirect(reverse('logout'))
            elif user.role == 'patient':
                if module_name in patient_permissions:
                    pass
                else:
                    return HttpResponseRedirect(reverse('logout'))
            else:
                return HttpResponseRedirect(reverse("login"))
        else:
            print(request.path)
            if module_name in anonymous_user_permission or request.path == reverse('patient:home'):
                pass
            else:
                return HttpResponseRedirect(reverse("login"))
