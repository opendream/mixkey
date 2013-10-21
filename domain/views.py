# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound

from domain.models import Project, Sensor, Data
from datetime import datetime

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
        except Sensor.DoesNotExist:
            pass
        
    data_list = data_list[0:30]


    # Summary
    project_list = []
    
    for project in project_query:
        
        sensor_list = []
        
        if sensor_selected:
            sensor_query = [sensor_selected]
        else:
            sensor_query = project.sensor_set.all()
        
        for sensor in sensor_query:
                        
            data = False
            try:
                data = sensor.data_set.order_by('-created')[0]
            except IndexError:
                pass
            
            if data:
                sensor_list.append((sensor, data))
        
        if sensor_list:   
            project_list.append((project, sensor_list))
        
    return render(request, 'overview.html', {
        'data_list': data_list, 
        'project_list': project_list,
        'sensor_selected': sensor_selected
    })

    
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
    