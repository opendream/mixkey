# -*- coding: utf-8 -*-

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.forms.models import model_to_dict

from domain.models import Project, Sensor, Data, DataTenMinute, DataThirtyMinute, DataHour, DataDay, DataWeek, DataMonth, DataYear, SMSLog
from domain.functions import medfilt1, set_to_midnight

from datetime import datetime, timedelta

import numpy as np
import copy

field_name_list = ['utrasonic', 'temperature', 'humidity', 'raingauge', 'battery']
field_label_list ={
    'utrasonic'  : 'Water Level (cm.)', 
    'temperature': 'Temperature (℃)', 
    'humidity'   : 'Humidity (%)', 
    'raingauge'  : 'Raingauge (mm.)', 
    'battery'    : 'Battery (%)'
}
inst_minutes = {
    'DataYear': 365*24*60,
    'DataMonth': 30*24*60,
    'DataWeek': 7*24*60,
    'DataDay': 1*24*60,
    'DataHour': 60,
    'DataThirtyMinute': 30,
    'DataTenMinute': 10,
    'Data': 1,
}
child_map = {
    'DataYear': 'DataMonth',
    'DataMonth': 'DataWeek',
    'DataWeek': 'DataDay',
    'DataDay': 'DataHour',
    'DataHour': 'DataThirtyMinute',
    'DataThirtyMinute': 'DataTenMinute',
    'DataTenMinute': 'Data',
    'Data': 'Data',
}

def home(request):
    # For mixkey create record
    if request.GET.get('M') or request.GET.get('m') or request.GET.get('S') or request.GET.get('s'):
        return data_create(request)
        
    return project_overview(request)

def sensor_overview(request, project_code, sensor_code):
    return project_overview(request, project_code, sensor_code)
    

def project_overview(request, project_code=False, sensor_code=False):        
        
    project_selected = request.META.get('PROJECT_SELECTED')
    
    if project_selected:
        project_query = [project_selected]
    else:
        project_query = Project.objects.all().order_by('-created')
        
    
    sensor_selected = None
    
    # List all data list
    data_list = Data.objects.all().order_by('-created')
    if project_selected:
        data_list = data_list.filter(sensor__project=project_selected)
        
        try:
            if sensor_code:
                sensor_selected = Sensor.objects.get(project=project_selected, code=sensor_code)
                data_list = data_list.filter(sensor=sensor_selected)
        except Sensor.DoesNotExist:
            pass
        
    data_list = data_list[0:30]


    # Summary
    project_list = []
    
    field_name = request.GET.get('field') or 'utrasonic'
    
    for project in project_query:
        
        sensor_list = []
        
        if sensor_selected:
            sensor_query = [sensor_selected]
        else:
            sensor_query = project.sensor_set.all()
        
        for sensor in sensor_query:
                        
            data = False
            sensor_data_list = sensor.data_set.order_by('-created')
                        
            sensor.data_summary = data_summary(sensor, op='DataDay', field_name=field_name)
            
            try:
                data = sensor_data_list[0]
            except IndexError:
                pass
            
            if data:
                sensor_list.append((sensor, data))
        
        if sensor_list:   
            project_list.append((project, sensor_list))
        
    return render(request, 'overview.html', {
        'data_list': data_list, 
        'project_list': project_list,
        'sensor_selected': sensor_selected,
        'field_name_list': field_name_list,
        'current_field': field_name
    })
    
    
def data_summary(sensor, op='DataDay', field_name='utrasonic'):
    
    # Define
    field_name_list = [f.name for f in Data._meta.fields]
    label = field_label_list[field_name]
    timezone = sensor.project.timezone
    
    InstCache = eval(op)
    
    # prepare cache
    cache_list = list(InstCache.objects.filter(sensor=sensor).order_by('-created')[0:500])
    cache_list.reverse()
    cache_list.append(InstCache(sensor=sensor, created=datetime.today()))
    
    lost_list = []
    try:
        lost_list = list(SMSLog.objects.filter(sensor=sensor, category=SMSLog.SENSOR_LOST, created__gte=cache_list[0].created).order_by('-created'))
    except InstCache.DoesNotExist:
        pass
    
    
    data_list = []
    lost_value = None
    for cache in cache_list:
        
        created = cache.created.strftime("new Date(%Y, %m-1, %d, %H+" + str(timezone) + ", %M)")
        value = getattr(cache, field_name)
        
        if field_name == 'utrasonic' and value is not None and sensor.formula:
            x = value
            value = eval(sensor.formula)
            
        #elif field_name == 'battery' and value is not None:
        #    value = float(12.5-value)/float(12.5-10.5)*100
        
        data = [created, value, None]
        
        
        if value is not None:
            lost_value = value
            
        # insert 1 row lost data
        while lost_list and lost_list[-1].created < cache.created:
            lost = lost_list.pop()
            
            data_list.append([(lost.created - timedelta(minutes=30)).strftime("new Date(%Y, %m-1, %d, %H+" + str(timezone) + ", %M)"), value, lost_value])
            data_list.append([(lost.created - timedelta(minutes=30)).strftime("new Date(%Y, %m-1, %d, %H+" + str(timezone) + ", %M)"), value, None])
                    
        data_list.append(data)
        
    
    cols = [
        {'id': 'date', 'label': 'Date', 'type': 'datetime'},
        {'id': 'main', 'label': label, 'type': 'number'},
        {'id': 'lost', 'label': 'Sensor Lost', 'type': 'number'}
    ]
    
    if field_name == 'utrasonic':
        length = len(data_list)
    
        if sensor.level_red:
            cols.append({'id': 'red', 'label': 'Red Level', 'type': 'number'})
            data_list = zip(*data_list)
            data_list.append([sensor.level_red]*length)
            data_list = zip(*data_list)
    
        if sensor.level_yellow:
            cols.append({'id': 'yellow', 'label': 'Yellow Level', 'type': 'number'})
            data_list = zip(*data_list)
            data_list.append([sensor.level_yellow]*length)
            data_list = zip(*data_list)
            
    # Prepare data to js    
    result = []
    for row in data_list:
        row = {'c': [ {'v': c} for c in row]}
        result.append(row)
    
    result = {'cols': cols, 'rows': result}
    
    return result

    
def data_create(request):
    
    # Prepare data
    
    project = request.GET.get('P') or request.GET.get('p') or 'UNKNOW'
    
    # Hot fixed hard code
    if project == 'SLKK':
        project = 'SLK'
    # End hot fixed
    
    project, created = Project.objects.get_or_create(code=project)
    
    sensor = request.GET.get('M') or request.GET.get('m') or request.GET.get('S') or request.GET.get('s')
    if not sensor:
        return HttpResponseNotFound('Error: Sensor must be required (M or S)')
        
    try:
        sensor = Sensor.objects.get(code=sensor)
    except:
        sensor = Sensor.objects.create(project=project, code=sensor)
        
    utrasonic = request.GET.get('U') or request.GET.get('u')
    if not utrasonic:
        return HttpResponseNotFound('Error: Utrasonic must be required (U)')
        
    utrasonic = int(utrasonic)
    
    # Normal case
    
    temperature = request.GET.get('T') or request.GET.get('t') or None
    if temperature:
        temperature = float(temperature)
        
    humidity = request.GET.get('H') or request.GET.get('h') or None
    if humidity:
        humidity = int(humidity)
    
    raingauge = request.GET.get('R') or request.GET.get('r') or None    
    if raingauge:
        raingauge = float(raingauge)
    
    battery = request.GET.get('B') or request.GET.get('b') or None
    if battery:
        battery = float(battery)
    
    data = Data.objects.create(sensor = sensor, utrasonic = utrasonic, temperature = temperature, humidity = humidity, raingauge = raingauge, battery = battery, created=datetime.today())
    
    
    return HttpResponse('Data store completed: project: %s, sensor: %s, utrasonic: %s, temperature: %s, humidity: %s, raingauge: %s, battery: %s' % (project.code, sensor.code, utrasonic, temperature, humidity, raingauge, battery))
    
