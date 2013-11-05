from django.db import models
from django.conf import settings

from domain.functions import median

from datetime import datetime, timedelta

TIME_ZONE_CHOICES = (
     (-12.0, '(GMT -12:00) Eniwetok, Kwajalein'),
     (-11.0, '(GMT -11:00) Midway Island, Samoa'),
     (-10.0, '(GMT -10:00) Hawaii'),
     (-9.0, '(GMT -9:00) Alaska'),
     (-8.0, '(GMT -8:00) Pacific Time (US &amp; Canada)'),
     (-7.0, '(GMT -7:00) Mountain Time (US &amp; Canada)'),
     (-6.0, '(GMT -6:00) Central Time (US &amp; Canada), Mexico City'),
     (-5.0, '(GMT -5:00) Eastern Time (US &amp; Canada), Bogota, Lima'),
     (-4.0, '(GMT -4:00) Atlantic Time (Canada), Caracas, La Paz'),
     (-3.5, '(GMT -3:30) Newfoundland'),
     (-3.0, '(GMT -3:00) Brazil, Buenos Aires, Georgetown'),
     (-2.0, '(GMT -2:00) Mid-Atlantic'),
     (-1.0, '(GMT -1:00 hour) Azores, Cape Verde Islands'),
     (0.0, '(GMT) Western Europe Time, London, Lisbon, Casablanca'),
     (1.0, '(GMT +1:00 hour) Brussels, Copenhagen, Madrid, Paris'),
     (2.0, '(GMT +2:00) Kaliningrad, South Africa'),
     (3.0, '(GMT +3:00) Baghdad, Riyadh, Moscow, St. Petersburg'),
     (3.5, '(GMT +3:30) Tehran'),
     (4.0, '(GMT +4:00) Abu Dhabi, Muscat, Baku, Tbilisi'),
     (4.5, '(GMT +4:30) Kabul'),
     (5.0, '(GMT +5:00) Ekaterinburg, Islamabad, Karachi, Tashkent'),
     (5.5, '(GMT +5:30) Bombay, Calcutta, Madras, New Delhi, Colombo'),
     (5.75, '(GMT +5:45) Kathmandu'),
     (6.0, '(GMT +6:00) Almaty, Dhaka'),
     (7.0, '(GMT +7:00) Bangkok, Hanoi, Jakarta'),
     (8.0, '(GMT +8:00) Beijing, Perth, Singapore, Hong Kong'),
     (9.0, '(GMT +9:00) Tokyo, Seoul, Osaka, Sapporo, Yakutsk'),
     (9.5, '(GMT +9:30) Adelaide, Darwin'),
     (10.0, '(GMT +10:00) Eastern Australia, Guam, Vladivostok'),
     (11.0, '(GMT +11:00) Magadan, Solomon Islands, New Caledonia'),
     (12.0, '(GMT +12:00) Auckland, Wellington, Fiji, Kamchatka')
)

ALERT_RED    = 1
ALERT_YELLOW = 2
ALERT_GREEN  = 3
DAILY        = 4
CATEGORY_CHOICES = (
    (ALERT_RED, 'RED'), 
    (ALERT_YELLOW, 'YELLOW'), 
    (ALERT_GREEN, 'GREEN'), 
    (DAILY, 'DAILY')
)

class Project(models.Model):
    
    code        = models.CharField(max_length=255, unique=True) # Required
    timezone    = models.FloatField(choices=TIME_ZONE_CHOICES, default=0.0)

    name        = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True)
        
    created     = models.DateTimeField(auto_now_add=True)
    
    # For SMS
    tel_key     = models.CharField(null=True, blank=True, max_length=255) # not use
    tel_list    = models.TextField(null=True, blank=True)
    data_dict   = models.TextField(null=True, blank=True)
    
    def get_name(self):
        return self.name or self.code
    
    def __unicode__(self):
        return self.get_name()
    
    
class Sensor(models.Model):
    
    project      = models.ForeignKey(Project) # Required
                 
    code         = models.CharField(max_length=255, unique=True) # Required
    formula      = models.CharField(null=True, blank=True, max_length=255)
    lat          = models.FloatField(null=True, blank=True)
    lng          = models.FloatField(null=True, blank=True)
                 
    name         = models.CharField(null=True, blank=True, max_length=255)
    description  = models.TextField(null=True, blank=True)
                 
    created      = models.DateTimeField(auto_now_add=True)
    
    # For rules alert SMS
    level_red    = models.FloatField(null=True, blank=True)
    level_yellow = models.FloatField(null=True, blank=True)
    data_dict    = models.TextField(null=True, blank=True)
    
    # For SMS
    tel_key     = models.CharField(null=True, blank=True, max_length=255) # not use
    tel_list    = models.TextField(null=True, blank=True)
    
        
    def get_name(self):
        return self.name or self.code
        
    def get_category(self):
        
        water_level = 0
        
        try:
            data = Data.objects.order_by('-created')[0]
            water_level = data.get_water_level
        except Data.DoesNotExist:
            pass

        if self.level_red and water_level >= self.level_red:
            return 'RED'
        elif self.level_yellow and water_level >= self.level_yellow:
            return 'YELLOW'

        return 'GREEN'
        
    def __unicode__(self):
        return self.get_name()

class BaseData(models.Model):
    
    sensor      = models.ForeignKey(Sensor)
    utrasonic   = models.IntegerField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    humidity    = models.IntegerField(null=True, blank=True)
    raingauge   = models.FloatField(null=True, blank=True)
    battery     = models.FloatField(null=True, blank=True)
    
    created     = models.DateTimeField()
    
    class Meta:
        abstract = True
    
    @property
    def get_water_level_raw(self):
        
        if self.sensor.formula:
            x = self.utrasonic
            water_level = eval(self.sensor.formula)
            
        else:
            water_level = self.utrasonic
        
        return water_level
        
    @property    
    def get_water_level(self):
                
        # List of the data previous in 10 miniutes
        time_prev_check = self.created-timedelta(minutes=settings.PREV_DATA_BUFFER_TIME)
    
        data_list = self.sensor.data_set.filter(created__gte=time_prev_check, created__lte=self.created).order_by('-created')
        water_level_list = [d.get_water_level_raw for d in data_list]
        return median(water_level_list)
    

            
    def get_category(self):
        
        sensor = self.sensor
        water_level = self.get_water_level
        
        if sensor.level_red and water_level >= sensor.level_red:
            return 'RED'
        elif sensor.level_yellow and water_level >= sensor.level_yellow:
            return 'YELLOW'

        return 'GREEN' 
    
    def get_local_created(self):
        return self.created + timedelta(hours=self.sensor.project.timezone)

    def __unicode__(self):
        return 'Sensor: %s at %s' % (self.sensor.get_name(), self.get_local_created().strftime("%Y-%m-%d %H:%M:%S"))
        
    def save(self, *args, **kwargs):
        super(BaseData, self).save(*args, **kwargs)
        from domain.tasks import send_alert
        #send_alert.delay(self.id)
        send_alert(self.id)
        
        
class SMSLog(models.Model):
    
    ALERT_RED    = 1
    ALERT_YELLOW = 2
    ALERT_GREEN  = 3
    DAILY        = 4
    SENSOR_LOST  = 5
    
    CATEGORY_CHOICES = (
        (ALERT_RED, 'RED'), 
        (ALERT_YELLOW, 'YELLOW'), 
        (ALERT_GREEN, 'GREEN'), 
        (DAILY, 'DAILY'),
        (SENSOR_LOST, 'SENSOR LOST')
    )
    
    project      = models.ForeignKey(Project) # Required
    sensor       = models.ForeignKey(Sensor, null=True) # use in alert
    
    category = models.IntegerField(choices=CATEGORY_CHOICES, default=DAILY)
    is_send  = models.BooleanField(default=settings.TWILIO_SEND_SMS)
    from_tel = models.CharField(max_length=255)
    to_tel   = models.TextField()
    message  = models.TextField()
    created  = models.DateTimeField()
    
    message_sid = models.TextField(null=True, blank=True) # stroe recived message sisd from service
    
    def get_local_created(self):
        return self.created + timedelta(hours=self.project.timezone)
    
    def __unicode__(self):
        return '[%s] %s at %s' % (self.get_category_display(), self.project.get_name(), self.get_local_created().strftime("%Y-%m-%d %H:%M:%S"))
    
class Data(BaseData):
    pass
# Cache data table
class DataTenMinute(BaseData):
    pass
class DataThirtyMinute(BaseData):
    pass
class DataHour(BaseData):
    pass
class DataDay(BaseData):
    pass
class DataWeek(BaseData):
    pass
class DataMonth(BaseData):
    pass
class DataYear(BaseData):
    pass