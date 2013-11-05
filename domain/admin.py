from django.contrib import admin
from domain.models import *

admin.site.register(Project)
admin.site.register(Sensor)
admin.site.register(SMSLog)
admin.site.register(Data)
admin.site.register(DataTenMinute)
admin.site.register(DataThirtyMinute)
admin.site.register(DataHour)
admin.site.register(DataDay)
admin.site.register(DataWeek)
admin.site.register(DataYear)

