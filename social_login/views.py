from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


def login(request):
    # send_mail(message='hello my good man', subject='testing mail server', from_email=settings.EMAIL_HOST_USER, recipient_list=['ebikdeli@yahoo.com', 'ebikdeli@gmail.com'])
    # print(settings.EMAIL_BACKEND)
    # from sendmail.tasks import sending_mail
    # result = sending_mail.delay('this is test mail', 'hello man you okay', 'ebikdeli@gmail.com', ['ebikdeli@gmail.com', 'ebikdeli@yahoo.com'])
    # print(result.get(timeout=30))
    return render(request, 'social_login/templates/login.html')


@login_required
def home(request):
    return render(request, 'social_login/templates/home.html')
