import datetime
import smtplib

import pytz
from django.core.mail import send_mail

from config import settings
from config.settings import EMAIL_HOST_USER
from mailings.models import Mailings, MailingAttempt

def send_mailing(mailing: Mailings, current_datetime):
    period= {
        'days': datetime.timedelta(hours=24),
        'weeks': datetime.timedelta(days=7),
        'months': datetime.timedelta(days=30)
    }
    try:
        send_mail(
            subject=mailing.message.title,
            message=mailing.message.text,
            from_email=EMAIL_HOST_USER,
            recipient_list=[i.email for i in mailing.clients.all()],
            fail_silently=False
        )
        MailingAttempt.objects.create(
            mailing=mailing,
            date_time=current_datetime,
            successful_attempt=True,
            next_send=current_datetime + period[mailing.period]
        )
    except smtplib.SMTPException as e:
        MailingAttempt.objects.create(
            mailing=mailing,
            date_time=current_datetime,
            successful_attempt=False,
            error_at=e,
            next_send=current_datetime + period[mailing.period]
        )


def my_scheduled_job():
    mailings = Mailings.objects.filter(status="active")
    print(mailings)
    for mailing in mailings:
        print(mailing)
        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime = datetime.datetime.now(zone)
        reports =  MailingAttempt.objects.filter(mailing=mailing)
        print(reports)
        print(current_datetime)
        if reports:
            last_report = reports.order_by('-date_time').first()
            if current_datetime >= last_report.next_send.astimezone(zone):
                send_mailing(mailing, current_datetime)
        else:
            if current_datetime >= mailing.date_time.astimezone(zone):
                send_mailing(mailing, current_datetime)




