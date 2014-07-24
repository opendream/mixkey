from django.conf import settings
from django.db.models import Q
from django.core.mail import send_mail

from domain.models import Project, Sensor, SMSLog, Data, DataTenMinute, DataThirtyMinute, DataHour, DataDay, DataWeek, DataMonth, DataYear, SMSLog
from domain.templatetags.domain_tags import cm2m

from celery.decorators import task
from datetime import date, time, datetime, timedelta
from dateutil.relativedelta import relativedelta

from twilio.rest import TwilioRestClient

import logging
import re
import numpy as np

@task()
def send_sms(project, message_body, category, sensor=None, created=None, subject=None):
    # Send message to tel list with Twilio
    message = None
    message_sid = []
    tel_list_log = []
        
    client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    tel_list = ''
    if sensor:
        if category in [SMSLog.ALERT_RED, SMSLog.ALERT_YELLOW, SMSLog.ALERT_GREEN, SMSLog.ALERT_BATTERY_RED, SMSLog.ALERT_BATTERY_YELLOW, SMSLog.ALERT_BATTERY_GREEN]:
            tel_list = sensor.tel_list or ''
        elif category in [SMSLog.SENSOR_LOST]:
            tel_list = settings.DETECT_SENSOR_LOST_TEL_LIST or ''
            
    else:
        tel_list = project.tel_list or ''
        
    email_list = []
    
    for tel_email in tel_list.split(','):
        
        tel_email = '%s|' % tel_email
        tel_email = tel_email.split('|')
        tel = tel_email[0].strip()
        email = tel_email[1].strip()
        
        if settings.TWILIO_SEND_SMS and tel:
        
            message = client.messages.create(body=message_body, to=tel, from_=settings.TWILIO_FROM_NUMBER)
            message_sid.append(message.sid)
            tel_list_log.append(tel)
        
        if email:
            email_list.append(email)
    
    message_sid = ','.join(message_sid)
    tel_list_log = ','.join(tel_list_log)
    
    
    if not subject:
        subject = message_body.split('\n')[0]
        
    send_mail(subject, message_body, settings.EMAIL_ADDRESS_NO_REPLY, email_list, fail_silently=False)
        
        
    if not created:
        created = datetime.today()
                    
    SMSLog.objects.create(project=project, sensor=sensor, category=category, is_send=settings.TWILIO_SEND_SMS, from_tel=settings.TWILIO_FROM_NUMBER, to_tel=tel_list_log, message=message_body, message_sid=message_sid, created=created)
    
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
            water_level_list = [data.get_water_level for data in data_list]
            
            if water_level_list:
                messages.append('Sensor %s -- max: %s cm., min: %s cm., average: %s cm.' % (sensor.get_name(), (max(water_level_list)), (min(water_level_list)), round(float(sum(water_level_list))/len(water_level_list), 2)))
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
    
def alert_message(category, project, sensor, value, text='water level: %s cm.'):
    
    return '\n'.join([
        '[%s CODE] from telemetry station' % SMSLog(category=category).get_category_display(),
        'Project: %s -- report reference from MSL.' % project.get_name(),
        ('Sensor %s -- ' + text) % (sensor.get_name(), value)     
    ])
    
    
@task()
def send_alert(data):
    
    # In case task cant send obj to function
    if type(data) == int or type(data) == long :
        data = Data.objects.get(id=data)
    
    sensor = data.sensor
    
    if not sensor.project.tel_list and not sensor.tel_list:
        return False
    
    latest_sms = False
    try:
        latest_sms = SMSLog.objects.filter(sensor=sensor).order_by('-created')[0]
        if data.created < latest_sms.created + timedelta(minutes=settings.PREV_DATA_BUFFER_TIME):
            return False
    except IndexError:
        pass
                
    project = data.sensor.project
    water_level_median = data.get_water_level
    
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
            latest_category = SMSLog.objects.filter(sensor=sensor, category__in=[SMSLog.ALERT_RED, SMSLog.ALERT_YELLOW, SMSLog.ALERT_GREEN]).order_by('-created')[0].category
            
            if latest_category == SMSLog.ALERT_RED or latest_category == SMSLog.ALERT_YELLOW:
                send_sms(project, alert_message(SMSLog.ALERT_GREEN, project, sensor, water_level_median), SMSLog.ALERT_GREEN, sensor, data.created)
        
        except IndexError:
            pass

@task()
def send_battery_alert(data):
    
    # In case task cant send obj to function
    if type(data) == int or type(data) == long :
        data = Data.objects.get(id=data)
    
    sensor = data.sensor
    
    
    if not sensor.project.tel_list and not sensor.tel_list:
        return False
    latest_sms = False
    try:
        latest_sms = SMSLog.objects.filter(sensor=sensor).order_by('-created')[0]
        if data.created < latest_sms.created + timedelta(minutes=settings.PREV_DATA_BUFFER_TIME):
            return False
    except IndexError:
        pass
            
    project = data.sensor.project
    battery_median = data.get_battery
      
    # List of repeat sms send in same category
    #time_prev_check_repeat = data.created-timedelta(minutes=settings.PREV_DATA_BUFFER_TIME*(settings.MAX_REPEAT_ALERT))
    log_list = SMSLog.objects.filter(sensor=sensor).order_by('-created')
  
    alert_text = 'battery: %s V.'
    
    # Red code alert limit in 5 times
    if battery_median <= settings.BATTERY_RED_LEVEL:
        if count_log_category(log_list[0: settings.MAX_REPEAT_ALERT], SMSLog.ALERT_BATTERY_RED) < settings.MAX_REPEAT_ALERT:
            send_sms(project, alert_message(SMSLog.ALERT_BATTERY_RED, project, sensor, battery_median, text=alert_text), SMSLog.ALERT_BATTERY_RED, sensor, data.created)
            
    # Yellow code alert limit in 5 times        
    elif battery_median <= settings.BATTERY_YELLOW_LEVEL and battery_median > settings.BATTERY_RED_LEVEL:
        if count_log_category(log_list[0: settings.MAX_REPEAT_ALERT], SMSLog.ALERT_BATTERY_YELLOW) < settings.MAX_REPEAT_ALERT:
            send_sms(project, alert_message(SMSLog.ALERT_BATTERY_YELLOW, project, sensor, battery_median, text=alert_text), SMSLog.ALERT_BATTERY_YELLOW, sensor, data.created)
            
    else:
        try:
            latest_category = SMSLog.objects.filter(sensor=sensor, category__in=[SMSLog.ALERT_BATTERY_RED, SMSLog.ALERT_BATTERY_YELLOW, SMSLog.ALERT_BATTERY_GREEN]).order_by('-created')[0].category
            
            if latest_category == SMSLog.ALERT_BATTERY_RED or latest_category == SMSLog.ALERT_BATTERY_YELLOW:
                send_sms(project, alert_message(SMSLog.ALERT_BATTERY_GREEN, project, sensor, battery_median, text=alert_text), SMSLog.ALERT_BATTERY_GREEN, sensor, data.created)
        
        except IndexError:
            pass
            
                        
@task()            
def detect_sensor_lost():
    
    for sensor in Sensor.objects.exclude(data=None):
        
        today = datetime.today()
        latest_data = sensor.data_set.latest('created')
     
        if (latest_data.created <= today - timedelta(minutes=settings.DETECT_SENSOR_LOST_TIME)) and (latest_data.created > today - timedelta(minutes=settings.DETECT_SENSOR_LOST_TIME*2)):
            messages = [
                'Detect sensor lost signal more than %s minutes.' % settings.DETECT_SENSOR_LOST_TIME,
                'Project %s -- Sensor %s.' % (sensor.project.get_name(), sensor.get_name())
            ]
            message_body = '\n'.join(messages)        
            
            print sensor.get_name()
            send_sms(sensor.project, message_body, SMSLog.SENSOR_LOST, sensor=sensor, created=today)

# Cache data

minutes_map_list = [
    ('DataYear', 365*24*60),
    ('DataMonth', 30*24*60),
    ('DataWeek', 7*24*60),
    ('DataDay', 1*24*60),
    ('DataHour', 60),
    ('DataThirtyMinute', 30),
    ('DataTenMinute', 10),
]

minutes_map = dict(minutes_map_list)

def get_datetime_label(op):
    label = re.findall('[A-Z][^A-Z]*', op)[-1].lower()
    if label == 'week':
        label = 'day'
    return label
    
def floor_time(dt, op):
    
    minutes = minutes_map[op]
    
    args = {'seconds': dt.second, 'microseconds': dt.microsecond}
    has_mt = False
    
    for key, step_minutes in minutes_map_list:
        
        label = get_datetime_label(key)
        mt = minutes/step_minutes
                        
        if mt > 0 and not has_mt:

            has_mt = True
            
            if minutes >= minutes_map['DataMonth']:
                mod = getattr(relativedelta(months=minutes/minutes_map['DataMonth']), '%ss' % label)
            else:
                mod = getattr(relativedelta(minutes=minutes), '%ss' % label)
            
            args['%ss' % label] = getattr(dt, label) % mod
            
            minutes = minutes - step_minutes
            
        elif mt <= 0 and has_mt and not args.get('%ss' % label):
            args['%ss' % label] = getattr(dt, label)
                        
    result = dt - relativedelta(**args)
    
    if op == 'DataWeek':
        result = result - timedelta(days=result.weekday())
    
    return result


def merge_data_field(data_list):
    
    if not data_list.size:
        return False
    
    field_name_list = ['utrasonic', 'temperature', 'humidity', 'raingauge', 'battery']
    
    
    data_step = dict(zip(field_name_list, [None]*len(field_name_list)))
    
    has_value = False
    
    for field_name in field_name_list:
        
        value_list = []
        for data in data_list:
            fv = getattr(data, field_name)
            if fv != None:
                value_list.append(fv)
                        
        value = None
        if value_list:
            value = sum(value_list) if field_name == 'raingauge' else np.mean(value_list)
        
        if value != None and not np.isnan(value):

            data_step[field_name] = value
            has_value = True
        
    return data_step if has_value else False

    
def build_cache():
    
    now = datetime.today()
    
    # Prepare data maping

    
    field_name_list = [f.name for f in Data._meta.fields]

    inst_list = ['Data', 'DataTenMinute', 'DataThirtyMinute', 'DataHour', 'DataDay', 'DataWeek', 'DataMonth', 'DataYear']

    pil = list(inst_list)
    pil.append(False)
    cil = list(inst_list)
    cil.insert(0, False)

    parent_map = dict(zip(cil, pil))
    del(parent_map[False])
    child_map = dict(zip(pil, cil))
    del(child_map[False])
    
    
    # Start loop of sensor list
    
    
    
    for sensor in Sensor.objects.all():
        
        inst = 'Data'
        
        while inst:
            
            inst = parent_map[inst]
            
            if not inst:
                continue

            # Prepare data
            data_list = eval(child_map[inst]).objects.filter(sensor=sensor).order_by('created')
            
            InstCache = eval(inst)
            try:
                cache_latest = InstCache.objects.filter(sensor=sensor).latest('created')
                data_list = data_list.filter(created__gt=cache_latest.created)
            except InstCache.DoesNotExist:
                cache_latest = None
                
            minutes = minutes_map[inst]
            
            # Check if can buid cache via dateime delta
            if cache_latest and now - cache_latest.created <= timedelta(minutes=minutes):
                continue
                
            data_list = data_list.values_list()

            if not data_list:
                continue
                
            data_list = np.core.records.fromrecords(data_list, names=field_name_list)
            
            cache_created_list = {}
                                
            for data in data_list:
                
                prev_time = floor_time(data.created-timedelta(minutes=minutes), inst)
                created   = floor_time(data.created, inst)
                
                if cache_created_list.get(created):
                    continue
                    
                step_list = data_list[((data_list['created'] > prev_time) & (data_list['created'] <= created))]
                step = merge_data_field(step_list)
                
                if not step:
                    continue
                    
                step['sensor'] = sensor
                step['created'] = created
                
                cache = InstCache(**step)
                cache.save()
                
                cache_created_list[created] = True
                
                    
                print 'Sensor -- %s, Inst -- %s, Date -- %s' % (sensor, inst, created)
            
            
            

