from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


class EmailNotifier:
    @staticmethod
    def send_ticket_assignment(ticket, user):
        ticket_url = f"{settings.BASE_URL}{reverse('tickets:details', args=[ticket.pk])}"
        subject = f'New Ticket Assignment: {ticket.title}'
        context = {
            'user': user,
            'ticket': ticket,
            'ticket_url': ticket_url
        }

        html_message = render_to_string('emails/ticket-assignment.html', context)
        plain_message = render_to_string('emails/ticket-assignment.txt', context)

        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False
        )

    @staticmethod
    def send_password_reset(user, request):
        subject = 'Password Reset Request'
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        context = {
            'user': user,
            'reset_url': request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )
        }

        html_message = render_to_string('emails/password-reset.html', context)
        plain_message = render_to_string('emails/password-reset.txt', context)

        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False
        )