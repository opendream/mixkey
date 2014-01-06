
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import DjangoAuthorization

from domain.models import Project, Sensor, Data, DataTenMinute, DataThirtyMinute, DataHour, DataDay, DataWeek, DataMonth, DataYear

class ProjectResource(ModelResource):
    
    class Meta:
        #always_return_data = True
        queryset = Project.objects.all().order_by('-created')
        resource_name = 'project'
        
        filtering = {
            'code'  : ALL_WITH_RELATIONS
        }
        ordering = {
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
        

class SensorResource(ModelResource):
    
    project = fields.ForeignKey(ProjectResource, 'project')
    
    class Meta:
        #always_return_data = True
        queryset = Sensor.objects.all().order_by('-created')
        resource_name = 'sensor'
        
        filtering = {
            'project' : ALL_WITH_RELATIONS,
            'code'    : ALL
        }
        ordering = {
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
        

base_data_filtering = {
    'sensor': ALL_WITH_RELATIONS,
    'project': ALL_WITH_RELATIONS,
    'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
}
base_data_ordering = {
    'created'  : ALL
}

class BaseDataResource(ModelResource):
    
    sensor = fields.ForeignKey(SensorResource, 'sensor')
    project = fields.ForeignKey(ProjectResource, 'sensor__project')
    

class DataResource(BaseDataResource):
    class Meta:
        queryset = Data.objects.all().order_by('-created')
        resource_name = 'data'
        
        filtering = base_data_filtering
        ordering = base_data_ordering
            
class DataTenMinuteResource(BaseDataResource):
    class Meta:
        queryset = DataTenMinute.objects.all().order_by('-created')
        resource_name = 'data_ten_minute'
        
        filtering = base_data_filtering
        ordering = base_data_ordering
        
class DataThirtyMinuteResource(BaseDataResource):
    class Meta:
        queryset = DataThirtyMinute.objects.all().order_by('-created')
        resource_name = 'data_thirty_minute'
        
        filtering = base_data_filtering
        ordering = base_data_ordering
        
class DataHourResource(BaseDataResource):
    class Meta:
        queryset = DataHour.objects.all().order_by('-created')
        resource_name = 'data_hour'
        
        filtering = base_data_filtering
        ordering = base_data_ordering
        
class DataDayResource(BaseDataResource):
    class Meta:
        queryset = DataDay.objects.all().order_by('-created')
        resource_name = 'data_day'
        
        filtering = base_data_filtering
        ordering = base_data_ordering
        
class DataWeekResource(BaseDataResource):
    class Meta:
        queryset = DataWeek.objects.all().order_by('-created')
        resource_name = 'data_week'
        
        filtering = base_data_filtering
        ordering = base_data_ordering
        
class DataMonthResource(BaseDataResource):
    class Meta:
        queryset = DataMonth.objects.all().order_by('-created')
        resource_name = 'data_month'
        
        filtering = base_data_filtering
        ordering = base_data_ordering
        
class DataYearResource(BaseDataResource):
    class Meta:
        queryset = DataYear.objects.all().order_by('-created')
        resource_name = 'data_year'
        
        filtering = base_data_filtering
        ordering = base_data_ordering
        