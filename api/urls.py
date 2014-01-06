from django.conf.urls import patterns, include

from api.resources import *

project_resource   = ProjectResource()
sensor_resource    = SensorResource()
data_resource      = DataResource()
data_ten_minute    = DataTenMinuteResource()
data_thirty_minute = DataThirtyMinuteResource()
data_hour          = DataHourResource()
data_day           = DataDayResource()
data_week          = DataWeekResource()
data_month         = DataMonthResource()
data_year          = DataYearResource()

urlpatterns = patterns('',
    (r'', include(project_resource.urls)),
    (r'', include(sensor_resource.urls)),
    (r'', include(data_resource.urls)),
    (r'', include(data_ten_minute.urls)),
    (r'', include(data_thirty_minute.urls)),
    (r'', include(data_hour.urls)),
    (r'', include(data_day.urls)),
    (r'', include(data_week.urls)),
    (r'', include(data_month.urls)),
    (r'', include(data_year.urls)),
)