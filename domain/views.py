# -*- coding: utf-8 -*-

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound

from domain.models import Project, Sensor, Data, DataDay, DataWeek, DataMonth, DataYear, SMSLog
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
                        
            sensor.data_summary = data_summary(sensor, sensor_data_list, method='DataDay', field_name=field_name)
            
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

def data_summary(sensor, data_list, method='DataDay', field_name='utrasonic'):
    
    
    method_map = {
        'DataYear': 365,
        'DataMonth': 30,
        'DataWeek': 7,
        'DataDay': 1,
    }
    
    InstCache = eval(method)
    
    # prepare cache
    cache_list = list(InstCache.objects.filter(sensor=sensor).order_by('-created'))
    
    # Performance case, cut rows of query only realtime not cache
    cache_latest_created = None
    try:
        cache_latest_created = cache_list[0].created        
        data_list = data_list.filter(created__gt=cache_latest_created)
    except IndexError:
        pass
    
    current_dt = datetime.today()
    current_dt_midnight = set_to_midnight(current_dt)
    origin_dt_midnight = current_dt_midnight
    
    # duration per value
    dpv = timedelta(days=method_map[method])
    
    # merge data from cache and realtime
    data_list = list(data_list.filter(created__lte=current_dt))
    
    try:
        dummy = copy.copy(data_list[0])
        dummy.created = set_to_midnight(dummy.created+timedelta(days=1))
        data_list.insert(0, dummy)
    except:
        pass

        

    
    
    summary_value_list = []
    summary_value = []
    
    summary_value_all_list = []
    summary_value_all = {}
    
    summary_dt_list = []
    summary_dt = []
    
    end = len(data_list)
    
    for i, data in enumerate(data_list):
                
        value = getattr(data, field_name)
        
        if current_dt_midnight < data.created:
            summary_value.append(value)
            
            # Generate all field
            for fn in field_name_list:
                try:
                    summary_value_all[fn]
                except:
                    summary_value_all[fn] = []
                    
                summary_value_all[fn].append(getattr(data, fn))
                
            summary_dt.append(data.created)
        
        if data.created <= current_dt_midnight or i == end-1 or data.created >= current_dt:

            current_dt_midnight = current_dt_midnight - dpv
            
            
            if not summary_value:
                summary_value = None
            else:
                try:
                    summary_value = np.mean(medfilt1(summary_value, 8))
                except TypeError:
                    summary_value = np.mean((summary_value))
            
            summary_value_list.append(summary_value)
            
            
            # Generate all field
            for fn in field_name_list:
                if not summary_value_all.get(fn):
                    summary_value_all[fn] = None
                else:
                    try:
                        summary_value_all[fn] = np.mean(medfilt1(summary_value_all[fn], 8))
                    except TypeError:
                        summary_value_all[fn] = np.mean((summary_value_all[fn]))
                        
                        
                summary_value_all_list.append(summary_value_all)

           
            if not summary_dt:
                summary_dt = current_dt_midnight
            else: 
                summary_dt = summary_dt[int(len(summary_dt)/2)]
                
            summary_dt = set_to_midnight(summary_dt)
            
            # create cache if not exist
            if (not cache_latest_created or summary_dt > cache_latest_created) and (summary_dt < origin_dt_midnight-timedelta(days=1)):
                try:
                    cache = InstCache.objects.get(sensor=sensor, created=summary_dt)
                except InstCache.DoesNotExist:
                    cache = InstCache.objects.create(sensor=sensor, created=summary_dt)
            
                if getattr(cache, field_name) == None:
                    setattr(cache, field_name, summary_value)
                    
                    # Generate all field
                    for fn in field_name_list:
                        setattr(cache, fn, summary_value_all[fn])
                    cache.save()
            
            summary_dt_list.append(summary_dt.strftime("new Date(%Y, %m, %d)"))
            
            
            
            summary_value = []
            summary_value_all = {}
            summary_dt = []
    
    label = field_label_list[field_name]
    

    # merge cache and realtime data 
    summary_value_list.extend([getattr(cache, field_name) for cache in cache_list])
    summary_dt_list.extend([cache.created.strftime("new Date(%Y, %m, %d)") for cache in cache_list])
        
    # calculate to water level
    if field_name == 'utrasonic' and sensor.formula:
        summary_value_list = [eval(sensor.formula) if x != None else x for x in summary_value_list]
            

    has_lost = False

    lost_list = list(SMSLog.objects.filter(sensor=sensor).order_by('-created'))
    if lost_list:
        length = len(summary_dt_list)
        summary_lost_list = [None]*length

        for lost in lost_list:
            try:
                i = summary_dt_list.index(lost.created.strftime("new Date(%Y, %m, %d)"))
                summary_dt_list.insert(i, lost.created.strftime("new Date(%Y, %m, %d, %H, %M)"))
                summary_value_list.insert(i, summary_value_list[i])
                summary_lost_list.insert(i, summary_value_list[i])
            except ValueError:
                has_lost = True
                     
                
    
    cols = []
    
    #add label to graph 
    cols.append({'id': 'date', 'label': 'Date', 'type': 'datetime'})
    cols.append({'id': 'main', 'label': label, 'type': 'number'})
    
    # flip graph left to right
    summary_value_list.reverse()
    summary_dt_list.reverse()
    
    
    
    #prepare data for google api chart
    summary_list = [summary_dt_list, summary_value_list]
    
    if False and has_lost:
        cols.append({'id': 'lost', 'label': 'Sensor Lost', 'type': 'number'})
        summary_lost_list.reverse()
        
        summary_list.append(summary_lost_list)
        
    # add red yellow line
    if field_name == 'utrasonic':
        
        length = len(summary_dt_list)
        
        if sensor.level_red:
            cols.append({'id': 'red', 'label': 'Red Level', 'type': 'number'})
            level_red_list = [sensor.level_red]*length
            summary_list.append(level_red_list)
        
        if sensor.level_yellow:
            cols.append({'id': 'yellow', 'label': 'Yellow Level', 'type': 'number'})
            level_yellow_list = [sensor.level_yellow]*length
            summary_list.append(level_yellow_list)
    
    summary_list = []
    for data in Data.objects.filter(sensor=sensor).order_by('-created')[0:500]:
        summary_list.append((data.created.strftime("new Date(%Y, %m, %d, %H, %M)"), data.get_water_level_raw))

        
    # Prepare data to js    
    result = []
    for row in summary_list:
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
    
