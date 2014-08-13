from django.contrib import admin
from daterange_filter.filter import DateTimeRangeForm, DateRangeForm, DateRangeFilter, DateTimeRangeFilter

from domain.models import *


admin.site.register(Project)
admin.site.register(Sensor)

class SMSLogAdmin(admin.ModelAdmin):
    list_filter = ('project', 'sensor', 'category', )
    list_display = ('project', 'sensor', 'category', 'created', )

admin.site.register(SMSLog, SMSLogAdmin)


class DataAdmin(admin.ModelAdmin):
    list_display = ('created', 'get_local_created', 'get_water_level_raw', 'utrasonic', 'temperature', 'humidity', 'raingauge', 'battery')
    #list_display = ('created', 'get_water_level', 'get_water_level_raw', 'utrasonic', 'temperature', 'humidity', 'raingauge', 'battery')
    list_filter = ('sensor', ('created', DateRangeFilter))
    actions = None


admin.site.register(Data, DataAdmin)
admin.site.register(DataTenMinute, DataAdmin)
admin.site.register(DataThirtyMinute, DataAdmin)
admin.site.register(DataHour, DataAdmin)
admin.site.register(DataDay, DataAdmin)
admin.site.register(DataWeek, DataAdmin)
admin.site.register(DataYear, DataAdmin)

