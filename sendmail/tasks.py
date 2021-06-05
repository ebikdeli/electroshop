from electroshop.settings.celery import app
from django.core.mail import send_mail


@app.task(name='adding to numbers')
def add(x, y):
    return x + y


@app.task(name='send mail')
def sending_mail(subject, message, from_email, recipients):
    sent = send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipients)
    return sent
