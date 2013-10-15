from django.contrib import admin
from domain.models import Project, Sensor, Data

admin.site.register(Project)
admin.site.register(Sensor)
admin.site.register(Data)

