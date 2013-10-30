from django.contrib import admin
from domain.models import Project, Sensor, Data, SMSLog, DataDay

admin.site.register(Project)
admin.site.register(Sensor)
admin.site.register(Data)
admin.site.register(SMSLog)
admin.site.register(DataDay)


