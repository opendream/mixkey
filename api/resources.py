# -*- coding: utf-8 -*-
from django.utils import feedgenerator
from django.utils.translation import check_for_language, ugettext as _
from django.contrib.sites.models import get_current_site
from django.conf import settings

from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import DjangoAuthorization
from tastypie.serializers import Serializer
from tastypie.cache import SimpleCache

from domain.models import Project, Sensor, Data, DataTenMinute, DataThirtyMinute, DataHour, DataDay, DataWeek, DataMonth, DataYear

import datetime
import csv
import cStringIO as StringIO

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

def prepare_data(item, prev_item=None):
    
    prev_item = prev_item or item
        
    created = datetime.datetime.strptime(item['created'], '%Y-%m-%dT%H:%M:%S')
    local_created = datetime.datetime.strptime(item['local_created'], '%Y-%m-%dT%H:%M:%S')
    
    
    #title = item['sensor']['name'] + ':' + _('utrasonic') + ' ' +  _('cm.') + ', ' + _('temperature') + ' ' + u'°C' + ', ' + _('humidity') + ' ' + '%' + ', '
    #title = item['sensor']['name'] + ':' + _('utrasonic') + _('cm.') + ', ' + _('temperature') + ' '  + u'°C' + ', ' + _('humidity') + ' ' + ('%d' % item['humidity']) + '%' + ', '
    title = item['sensor']['name'] + ' : ' + \
    _('utrasonic') + ' ' + ('%d' % item['utrasonic']) + ' ' + _('cm.') + ', ' + \
    _('temperature') + ' ' + ('%d' % item['temperature']) + u'°C' + ', ' + \
    _('humidity') + ' ' + ('%d' % item['humidity']) + '%' + ', ' + \
    _('date') + ' ' + ('%s' % local_created.strftime('%Y.%m.%d %H:%M:%S'))
    
    
    link = ''.join(['http://', get_current_site(None).domain, settings.STATIC_URL, 'image/', item['difference_status'], '.jpg'])
    
    #created.strftime('%Y.%m.%d %H:%M:%S'))

    return {
        'title': title, 
        'link': link, 
        'description': title,
        'pubdate': created,
        'updatedate': created
        
    }
    
class DataRSSSerializer(Serializer):
    formats = ['json', 'jsonp', 'xml', 'yaml', 'html', 'csv', 'plist', 'rss']
    content_types = {
        'json': 'application/json',
        'jsonp': 'text/javascript',
        'xml': 'application/xml',
        'yaml': 'text/yaml',
        'html': 'text/html',
        'csv': 'text/csv',
        'plist': 'application/x-plist',
        'rss': 'application/rss+xml',
    }
    
    def to_rss(self, data, options=None):
        
        
        options = options or {}
        rss_items = []
        data = self.to_simple(data, options)
        feed = feedgenerator.Rss201rev2Feed(
            title =u"MixKey Data RSS Feed",
            link=u'http://' + get_current_site(None).domain,
            description=u"MixKey Data RSS Feed Update"
        )
        
        try:
            
            for item in data['objects']:
                feed.add_item(**prepare_data(item))

        except KeyError:
            
            item = data
            feed.add_item(**prepare_data(item))
        
        return feed.writeString('utf-8')
    
    def to_csv(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)

        csvfile = StringIO.StringIO()
        
        fieldnames = data['objects'][0].keys()
        fieldnames.append('sensor_code')
        
        
        dw = csv.DictWriter(csvfile, fieldnames)
        dw.writeheader();
        
        for row in data['objects']:
                        
            row['sensor_code'] = row['sensor']['code']
            row['sensor'] = row['sensor'].get('name').encode('utf-8')
                        
            dw.writerow(row)

        return csvfile.getvalue()
        
class BaseDataResource(ModelResource):
    
    sensor = fields.ForeignKey(SensorResource, 'sensor', full=True)
    project = fields.ForeignKey(ProjectResource, 'sensor__project')
    
    water_level = fields.FloatField(attribute='get_water_level')
    difference_status = fields.CharField(attribute='get_difference_status')
    created = fields.DateTimeField(attribute='created')
    local_created = fields.DateTimeField(attribute='get_local_created')

    def get_list(self, request, **kwargs):
        """
        Returns a serialized list of resources.

        Calls ``obj_get_list`` to provide the data, then handles that result
        set and serializes it.

        Should return a HttpResponse (200 OK).
        """
        # TODO: Uncached for now. Invalidation that works for everyone may be
        #       impossible.
        base_bundle = self.build_bundle(request=request)
        objects = self.cached_obj_get_list(bundle=base_bundle, **self.remove_api_resource_names(kwargs))
        sorted_objects = self.apply_sorting(objects, options=request.GET)

        paginator = self._meta.paginator_class(request.GET, sorted_objects, resource_uri=self.get_resource_uri(),
                                               limit=self._meta.limit, max_limit=self._meta.max_limit,
                                               collection_name=self._meta.collection_name)
        to_be_serialized = paginator.page()

        # Dehydrate the bundles in preparation for serialization.
        bundles = []

        for obj in to_be_serialized[self._meta.collection_name]:
            bundle = self.build_bundle(obj=obj, request=request)
            bundles.append(self.full_dehydrate(bundle, for_list=True))

        to_be_serialized[self._meta.collection_name] = bundles
        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
        return self.create_response(request, to_be_serialized)
    


class DataResource(BaseDataResource):
    class Meta:
        queryset = Data.objects.all().order_by('-created').prefetch_related('sensor', 'sensor__project')
        resource_name = 'data'
        
        filtering = base_data_filtering
        ordering = base_data_ordering
        serializer = DataRSSSerializer()

        cache = SimpleCache(timeout=60*10)

            
class DataTenMinuteResource(BaseDataResource):
    class Meta:
        queryset = DataTenMinute.objects.all().order_by('-created').prefetch_related('sensor', 'sensor__project')
        resource_name = 'data_ten_minute'
        
        filtering = base_data_filtering
        ordering = base_data_ordering

        cache = SimpleCache(timeout=60*10)

class DataThirtyMinuteResource(BaseDataResource):
    class Meta:
        queryset = DataThirtyMinute.objects.all().order_by('-created').prefetch_related('sensor', 'sensor__project')
        resource_name = 'data_thirty_minute'
        
        filtering = base_data_filtering
        ordering = base_data_ordering

        cache = SimpleCache(timeout=60*30)

class DataHourResource(BaseDataResource):
    class Meta:
        queryset = DataHour.objects.all().order_by('-created').prefetch_related('sensor', 'sensor__project')
        resource_name = 'data_hour'
        
        filtering = base_data_filtering
        ordering = base_data_ordering

        cache = SimpleCache(timeout=60*60)
        
class DataDayResource(BaseDataResource):
    class Meta:
        queryset = DataDay.objects.all().order_by('-created').prefetch_related('sensor', 'sensor__project')
        resource_name = 'data_day'
        
        filtering = base_data_filtering
        ordering = base_data_ordering

        cache = SimpleCache(timeout=60*60*24)
        
class DataWeekResource(BaseDataResource):
    class Meta:
        queryset = DataWeek.objects.all().order_by('-created').prefetch_related('sensor', 'sensor__project')
        resource_name = 'data_week'
        
        filtering = base_data_filtering
        ordering = base_data_ordering

        cache = SimpleCache(timeout=60*60*24*7)
        
class DataMonthResource(BaseDataResource):
    class Meta:
        queryset = DataMonth.objects.all().order_by('-created').prefetch_related('sensor', 'sensor__project')
        resource_name = 'data_month'
        
        filtering = base_data_filtering
        ordering = base_data_ordering

        cache = SimpleCache(timeout=60*60*24*30)
        
class DataYearResource(BaseDataResource):
    class Meta:
        queryset = DataYear.objects.all().order_by('-created').prefetch_related('sensor', 'sensor__project')
        resource_name = 'data_year'
        
        filtering = base_data_filtering
        ordering = base_data_ordering

        cache = SimpleCache(timeout=60*60*24*364)
        
