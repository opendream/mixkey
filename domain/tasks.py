from django.conf import settings
from django.db.models import Q

from domain.models import Project, Data, SMSLog
from domain.templatetags.domain_tags import cm2m

from celery.decorators import task
from datetime import date, time, datetime, timedelta

from twilio.rest import TwilioRestClient

import logging

@task()
def send_sms(project, message_body, category, sensor=None, created=None):
    # Send message to tel list with Twilio
    message = None
    message_sid = []
    if settings.TWILIO_SEND_SMS:
        
        client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        tel_list = []
        if sensor:
            tel_list = sensor.tel_list.split(',')
        else:
            tel_list = project.tel_list.split(','):
            
        for tel in tel_list:
            
            tel = tel.strip()
            message = client.messages.create(body=message_body, to=tel, from_=settings.TWILIO_FROM_NUMBER)
            message_sid.append(message.sid)
        
        message_sid = ','.join(message_sid)
        
        
    if not created:
        created = datetime.today()
                    
    SMSLog.objects.create(project=project, sensor=sensor, category=category, is_send=settings.TWILIO_SEND_SMS, from_tel=settings.TWILIO_FROM_NUMBER, to_tel=project.tel_list, message=message_body, message_sid=message_sid, created=created)
    
    return message
    
@task()
def send_daily():
        
    # Send notiy sms daily
    project_list = Project.objects.exclude(Q(tel_list__isnull=True) | Q(tel_list__exact='') | Q(tel_list='') | Q(tel_list='0'))
    
    # For production
    yesterday_midnight = datetime.combine(date.today(), time(23, 59, 59))-timedelta(days=1)
    
    # For test in todat midnight
    #yesterday_midnight = datetime.combine(date.today(), time(23, 59, 59))
    
    yesterday = yesterday_midnight-timedelta(days=1)
    
    for project in project_list:

        
        messages = [
            'Daily update from telemetry station util yesterday midnight.',
            'Project: %s -- report reference from MSL.' % project.get_name()
        ]
        
        for sensor in project.sensor_set.all():
            
            data_list = sensor.data_set.filter(created__gt=yesterday, created__lte=yesterday_midnight)
            water_level_list = [data.get_water_level() for data in data_list]
            
            if water_level_list:
                messages.append('Sensor %s -- max: %s m., min: %s m., average: %s m.' % (sensor.get_name(), cm2m(max(water_level_list)), cm2m(min(water_level_list)), cm2m(float(sum(water_level_list))/len(water_level_list))))
            else:
                messages.append('Sensor %s -- no data recorded, something problems, please check the sensor.' % (sensor.get_name()))
                
        message_body = '\n'.join(messages)
        
        
        send_sms(project, message_body, SMSLog.DAILY)
        


def count_log_category(log_list, category):
    count = 0
    for log in log_list:
        if log.category == category:
            count = count + 1
    return count
    
def alert_message(category, project, sensor, water_level_median):
    
    return '\n'.join([
        '[%s CODE] from telemetry station' % SMSLog(category=category).get_category_display(),
        'Project: %s -- report reference from MSL.' % project.get_name(),
        'Sensor %s -- water level: %s m.' % (sensor.get_name(), cm2m(water_level_median))     
    ])
    
    
@task()
def send_alert(data):
    
    # In case task cant send obj to function
    if type(data) == int or type(data) == long :
        data = Data.objects.get(id=data)
    
    sensor = data.sensor
    
    if not sensor.project.tel_list:
        return False
    
    latest_sms = False
    try:
        latest_sms = SMSLog.objects.filter(sensor=sensor).order_by('-created')[0]
        if data.created < latest_sms.created + timedelta(minutes=settings.PREV_DATA_BUFFER_TIME):
            return False
    except IndexError:
        pass
            
    
    project = data.sensor.project
    water_level_median = data.get_water_level()
    
    #water_level_median = median(water_level_list)
  
    # List of repeat sms send in same category
    #time_prev_check_repeat = data.created-timedelta(minutes=settings.PREV_DATA_BUFFER_TIME*(settings.MAX_REPEAT_ALERT))
    log_list = SMSLog.objects.filter(sensor=sensor).order_by('-created')
  
    
    # Red code alert limit in 5 times
    if water_level_median >= sensor.level_red:
        if count_log_category(log_list[0: settings.MAX_REPEAT_ALERT], SMSLog.ALERT_RED) < settings.MAX_REPEAT_ALERT:
            send_sms(project, alert_message(SMSLog.ALERT_RED, project, sensor, water_level_median), SMSLog.ALERT_RED, sensor, data.created)
            
    # Yellow code alert limit in 5 times        
    elif water_level_median >= sensor.level_yellow and water_level_median < sensor.level_red:
        if count_log_category(log_list[0: settings.MAX_REPEAT_ALERT], SMSLog.ALERT_YELLOW) < settings.MAX_REPEAT_ALERT:
            send_sms(project, alert_message(SMSLog.ALERT_YELLOW, project, sensor, water_level_median), SMSLog.ALERT_YELLOW, sensor, data.created)
            
    else:
        try:
            latest_category = SMSLog.objects.filter(sensor=sensor).order_by('-created')[0].category
            
            if latest_category == SMSLog.ALERT_RED or latest_category == SMSLog.ALERT_YELLOW:
                send_sms(project, alert_message(SMSLog.ALERT_GREEN, project, sensor, water_level_median), SMSLog.ALERT_GREEN, sensor, data.created)
        
        except IndexError:
            pass
    






