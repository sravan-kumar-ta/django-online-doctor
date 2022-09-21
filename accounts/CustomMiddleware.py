from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

admin_permissions = [
    'django.views.static',
    'django.contrib.auth.views',
    'django.contrib.admin.sites',
    'django.contrib.admin.options',
    'accounts.views',
    'django.contrib.auth.admin',
]

doctor_permissions = [
    'django.views.static',
    'accounts.views',
    'doctors.views',
    'blogs.views',
    'chat.views',
]

patient_permissions = [
    'patients.views',
    'accounts.views',
    'django.views.static',
    'blogs.views',
    'chat.views',
]

anonymous_user_permission = [
    'allauth.account.views',
    'django.contrib.auth.views',
    'django.contrib.admin.sites',
    'accounts.views',
    'blogs.views',
    'allauth.socialaccount.providers.oauth2.views',
    'rest_framework_simplejwt.views',
    'api.blogs_and_users_view',
    'api.doctor_view',
    'django_rest_passwordreset.views',
    'api.patient_view',
    'django.views.static',
    'django.views.generic.base',
    'drf_yasg.views',
    'api.social_auth_view',
]


class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        module_name = view_func.__module__
        print(module_name)
        print(request.path)
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
            if module_name in anonymous_user_permission or request.path == reverse('patient:home'):
                pass
                print("inner")
            else:
                return HttpResponseRedirect(reverse("login"))
