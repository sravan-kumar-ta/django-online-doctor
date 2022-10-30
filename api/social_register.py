import random

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import APIException

from accounts.CustomBackend import CustomAuth
from accounts.models import CustomUser


def generate_username(name):
    username = "".join(name.split(' ')).lower()
    if not CustomUser.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def auth_response(email):
    user = CustomAuth.authenticate(username=email, password='Pa$$w0rd!')

    if user:
        return {
            'username': user.username,
            'email': user.email,
            'tokens': user.tokens()
        }
    else:
        raise AuthenticationFailed(detail='Something wrong..!')


def register_social_user(provider, email, name, first_name, last_name):
    filtered_user_by_email = CustomUser.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:
            return auth_response(email)
        else:
            raise APIException({'error_message': 'Please continue your login using ' + filtered_user_by_email[0].auth_provider})

    else:
        user = {
            'username': generate_username(name),
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': 'Pa$$w0rd!'
        }
        user = CustomUser.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        return auth_response(email)
