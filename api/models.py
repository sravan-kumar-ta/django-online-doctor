from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    full_name = reset_password_token.user.get_full_name()
    header = 'Hai {},\n\n\tUpon your request, we send you a password reset token.\n\n\t'.format(full_name)
    message = 'Please copy the following token key:\n'
    key = reset_password_token.key
    footer = '\n\nThanks for using our site!'
    email_plaintext_message = "{}{}Token = {}{}".format(header, message, key, footer)
    send_mail(
        subject="Password Reset for {title}".format(title="Online doctor"),
        message=email_plaintext_message,
        from_email="exsample@somehost.local",
        recipient_list=[reset_password_token.user.email],
    )

#     starting = 'Hai user, \n\n\tUpon your request, we send you a password reset link. \n\n'
#     link = 'http://localhost:4200/password_reset/confirm/'
#     key = reset_password_token.key
#     ending = '\n\nThank you...'
#     email_plaintext_message = "{}{}?token={}{}".format(starting, link, key, ending)
#     # email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-confirm'),
#     #                                                reset_password_token.key)
#
#     send_mail(
#         subject="Password Reset for {title}".format(title="Online doctor"),
#         message=email_plaintext_message,
#         from_email="exsample@somehost.local",
#         recipient_list=[reset_password_token.user.email],
#     )
