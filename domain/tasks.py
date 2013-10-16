from django.conf import settings
from django.db.models import Q

from domain.models import Project, Data, SMSLog

from celery.decorators import task
from datetime import date, time, datetime, timedelta

from twilio.rest import TwilioRestClient

import logging


def send_sms(project, message_body, category):
    # Send message to tel list with Twilio
    message = None
    message_sid = None
    if settings.TWILIO_SEND_SMS:
        client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(body=message_body, to=project.tel_list, from_=settings.TWILIO_FROM_NUMBER)
        message_sid = message.sid
                    
    SMSLog.objects.create(project=project, category=category, is_send=settings.TWILIO_SEND_SMS, from_tel=settings.TWILIO_FROM_NUMBER, to_tel=project.tel_list, message=message_body, message_sid=message_sid)
    
    return message
    
@task()
def send_daily():
        
    # Send notiy sms daily
    project_list = Project.objects.exclude((Q(tel_key__isnull=True) | Q(tel_key__exact='') | Q(tel_key='') | Q(tel_key='0')) | (Q(tel_list__isnull=True) | Q(tel_list__exact='') | Q(tel_list='') | Q(tel_list='0')))
    
    # For production
    # yesterday_midnight = datetime.combine(date.today(), time(23, 59, 59))-timedelta(days=1)
    
    # For test in todat midnight
    yesterday_midnight = datetime.combine(date.today(), time(23, 59, 59))
    
    yesterday = yesterday_midnight-timedelta(days=1)
    
    for project in project_list:

        
        messages = ['Daily update from telemetry station util yesterday midnight.']
        
        for sensor in project.sensor_set.all():
            
            data_list = sensor.data_set.filter(created__gt=yesterday, created__lte=yesterday_midnight)
            water_level_list = [data.get_water_level() for data in data_list]
            
            if water_level_list:
                messages.append('Sensor %s -- max: %s, min: %s, average: %s' % (sensor.get_name(), max(water_level_list), min(water_level_list), float(sum(water_level_list))/len(water_level_list)))
            else:
                messages.append('Sensor %s -- no data recorded, something problems, please check the sensor.' % (sensor.get_name()))
                
        message_body = '\n'.join(messages)
        
        
        send_sms(project, message_body, SMSLog.DAILY)