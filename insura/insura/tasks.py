from .celery import app
from django.core.mail import send_mail
from insura.settings import EMAIL_ADDR_FROM


@app.task(name='sendmail')
def send_email_task(subject, message, email):
    send_mail(subject, message, EMAIL_ADDR_FROM, [email], fail_silently=False)
