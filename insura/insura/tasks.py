import time
from .celery import app
from django.core.mail import send_mail


@app.task
def send_email_task(email, subject, message):

    time.sleep(5)

    return send_mail(
        subject,
        message,
        'ors3000@mail.ru',
        [email],
        fail_silently=False,
    )
