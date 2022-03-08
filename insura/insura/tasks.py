from .celery import app
from market.services import SendMailService


@app.task(name='sendmail')
def send_email_task(email, subject, company, uname, umail):
    SendMailService.sendmail(email, subject, company, uname, umail)
