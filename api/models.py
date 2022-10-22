from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    starting = 'Hai user, \n\n\tUpon your request, we send you a password reset link. \n\n'
    link = 'http://localhost:4200/password_reset/confirm/'
    key = reset_password_token.key
    ending = '\n\nThank you...'
    email_plaintext_message = "{}{}?token={}{}".format(starting, link, key, ending)
    # email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-confirm'),
    #                                                reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Online doctor"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
