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
    'battery'    : 'Battery (V)'
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
                        
            sensor.data_summary = data_summary(sensor, sensor_data_list, op='DataDay', field_name=field_name)
            
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

def sensor_get_lost_list(sensor):
    SMSLog.objects.filter(sensor=sensor).order_by('-created')


def merge_data_field(data_list):
    data_step = dict(zip(field_name_list, [None]*len(field_name_list)))

    if data_list.size:
        for field_name in field_name_list:
            
            value_list = []
            for data in data_list:
                fv = getattr(data, field_name)
                if fv != None:
                    value_list.append(fv)
                    
            field_type = Data._meta.get_field(field_name).get_internal_type()
            
            value = None
            if value_list:
                value = sum(value_list) if field_name == 'raingauge' else np.mean(value_list)
            
            if value != None and not np.isnan(value):

                data_step[field_name] = value
            
    return data_step

def data_set_step_object(cdl, sensor, op, created):
        
    DataInst = eval(op)
    
    child_op = child_map[op]
    #DataInstChild = eval(child_op)
    
    minutes = inst_minutes[op]
    prev_time = created-timedelta(minutes=minutes)
    
    cdlc = cdl[child_op]
    
    try:
        data_list = cdlc[((cdlc['created'] >= prev_time) & (cdlc['created'] < created))]
        #data_list = list(DataInstChild.objects.filter(sensor=sensor,created__gte=prev_time, created__lt=created).order_by('-created'))
    except TypeError:
        data_list = np.array([])
        
    if op != 'Data' and not data_list.size:
        curr = created
        
        data_list = []
        while curr >= prev_time:
            tmp = data_get_step_object(cdl, sensor, child_op, curr)
            tmp = tmp.tolist()
            data_list.append(tmp)
            curr = curr - timedelta(minutes=inst_minutes[child_op])
        
        data_list = np.core.records.fromrecords(data_list, names=[f.name for f in Data._meta.fields])
        
    data_step = merge_data_field(data_list)
    data_step['sensor'] = sensor
    data_step['created'] = prev_time
    
    data_inst = DataInst(**data_step)
    if data_list.size and created - data_list[-1].created > timedelta(minutes=minutes):
        data_inst.save()
    else:
        data_inst.id = None
    
    data_inst_dict = model_to_dict(data_inst)
    data_inst = []
    for f in Data._meta.fields:
        data_inst.append(data_inst_dict[f.name])
        
    data_inst = np.core.records.fromrecords([data_inst], names=[f.name for f in Data._meta.fields])

    return data_inst[0]
        

def data_get_step_object(cdl, sensor, op, created):
    minutes = inst_minutes[op]
    
    prev_time = created-timedelta(minutes=minutes)
    #DataInst = eval(op)
    
    cdld = cdl[op]
    
    try:
        data_list = cdld[((cdld['created'] >= prev_time) & (cdld['created'] < created))]
        #data_list = list(DataInst.objects.filter(sensor=sensor, created__gte=prev_time, created__lt=created))
    except TypeError:
        data_list = np.array([])
    
    if not data_list.size:
        return data_set_step_object(cdl, sensor, op, created)
    else:
        return data_list[0]
        
    
    
def data_summary(sensor, data_list, op='DataDay', field_name='utrasonic', limit=200):
    
    timezone = sensor.project.timezone
        
    DataInst = eval(op)
    cache_list = DataInst.objects.filter(sensor=sensor).order_by('-created')
    
    try:
        data_list.filter(created__gt=cache_list[0].created)
    except IndexError:
        pass
        
    
    cdl = {}
    inst = op
    while (inst != 'Data'):
        cdl[inst] =  eval(inst).objects.filter(sensor=sensor).order_by('-created').values_list()
        if cdl[inst]:
            cdl[inst] = np.core.records.fromrecords(cdl[inst], names=[f.name for f in Data._meta.fields])

        inst = child_map[inst]
    
    cdl['Data'] = Data.objects.filter(sensor=sensor).order_by('-created').values_list()
    cdl['Data'] = np.core.records.fromrecords(cdl['Data'], names=[f.name for f in Data._meta.fields])
    
    data_list = cdl['Data']
            
    
    result = []
    latest_sdata = []
    
    curr_sdata = False
    
    for data in data_list:
        sdata = data_get_step_object(cdl, sensor, op, data.created)
        #from db
        if sdata.id and (not curr_sdata or sdata.id != curr_sdata.id):
            curr_sdata = sdata
            result.append(sdata)
        #from memory
        elif not sdata.id:
            latest_sdata.append(sdata)
    
    if latest_sdata:
        latest_sdata = merge_data_field(latest_sdata)
        result.insert(0, latest_sdata)    
        
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
    
