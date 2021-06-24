from electroshop.settings.celery import app
from django.core.mail import send_mail


@app.task(name='adding to numbers')
def add(x, y):
    return x + y


@app.task(name='sending checkout mail to customer')
def send_checkout_mail(subject, message, from_email, recipients, html_message=None):
    sent = send_mail(subject=subject, message=message, from_email=from_email,
                     recipient_list=recipients, html_message=html_message)
    return sent
