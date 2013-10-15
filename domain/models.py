from django.db import models

class Project(models.Model):
    
    code        = models.CharField(max_length=255, unique=True) # Required
    name        = models.CharField(null=True, max_length=255)
    description = models.TextField(blank=True)
    
    created     = models.DateTimeField(auto_now_add=True)
    
    
class Sensor(models.Model):
    
    project     = models.ForeignKey(Project) # Required
    
    code        = models.CharField(max_length=255, unique=True) # Required
    formula     = models.CharField(null=True, max_length=255)
    lat         = models.FloatField(null=True)
    lng         = models.FloatField(null=True)
               
    name        = models.CharField(null=True, max_length=255)
    description = models.TextField(blank=True)
    
    created     = models.DateTimeField(auto_now_add=True)
     

class Data(models.Model):
    
    sensor      = models.ForeignKey(Sensor)
    utrasonic   = models.IntegerField()          # Required
    temperature = models.FloatField(null=True)
    humidity    = models.IntegerField(null=True)
    raingauge   = models.FloatField(null=True)
    battery     = models.FloatField(null=True)
    
    created     = models.DateTimeField(auto_now_add=True)
