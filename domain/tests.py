from django.test import TestCase
from django.conf import settings

from datetime import date, timedelta, datetime
from domain.models import Project, Sensor, Data, SMSLog

class DomainTestAlert(TestCase):
    
    def setUp(self):
        self.buftime = settings.PREV_DATA_BUFFER_TIME
        
        self.p1 = Project.objects.create(code='p1', tel_list='+94710423088')
        self.s1  = Sensor.objects.create(code='s1', project=self.p1, level_red=90, level_yellow=80)
        
        
    def test_yellow_send_repeat_limit(self):
        
        today = datetime.today()
        
        indexs = range(0, 60)
        indexs.reverse()
        for i in indexs:
            Data.objects.create(sensor=self.s1, utrasonic=80, created=today-timedelta(minutes=i))
                
        self.assertEqual(5, SMSLog.objects.filter(category=SMSLog.ALERT_YELLOW).count())
        

    def test_red_send_repeat_limit(self):
        
        today = datetime.today()
        
        indexs = range(0, 60)
        indexs.reverse()
        for i in indexs:
            Data.objects.create(sensor=self.s1, utrasonic=90, created=today-timedelta(minutes=i))
                
        self.assertEqual(5, SMSLog.objects.filter(category=SMSLog.ALERT_RED).count())
        
        
    def test_green_send_repeat_limit(self):
        
        today = datetime.today()
        
        indexs = range(50, 60)
        indexs.reverse()
        for i in indexs:
            Data.objects.create(sensor=self.s1, utrasonic=30, created=today-timedelta(minutes=i))
            
        indexs = range(30, 40)
        indexs.reverse()
        for i in indexs:
            Data.objects.create(sensor=self.s1, utrasonic=80, created=today-timedelta(minutes=i))
            
        indexs = range(0, 30)
        indexs.reverse()
        for i in indexs:
            Data.objects.create(sensor=self.s1, utrasonic=70, created=today-timedelta(minutes=i))
            
                
        self.assertEqual(1, SMSLog.objects.filter(category=SMSLog.ALERT_GREEN).count())
        
        
    def test_peek_error(self):
        
        today = datetime.today()
        
        Data.objects.create(sensor=self.s1, utrasonic=40, created=today-timedelta(minutes=9))
        Data.objects.create(sensor=self.s1, utrasonic=43, created=today-timedelta(minutes=8))
        Data.objects.create(sensor=self.s1, utrasonic=45, created=today-timedelta(minutes=7))
        Data.objects.create(sensor=self.s1, utrasonic=40, created=today-timedelta(minutes=6))
        Data.objects.create(sensor=self.s1, utrasonic=85, created=today-timedelta(minutes=5)) # peek
        Data.objects.create(sensor=self.s1, utrasonic=43, created=today-timedelta(minutes=4))
        Data.objects.create(sensor=self.s1, utrasonic=45, created=today-timedelta(minutes=3))
        Data.objects.create(sensor=self.s1, utrasonic=40, created=today-timedelta(minutes=2))
        Data.objects.create(sensor=self.s1, utrasonic=41, created=today-timedelta(minutes=1))
        Data.objects.create(sensor=self.s1, utrasonic=95, created=today-timedelta(minutes=0)) # peek
                
        self.assertEqual(0, SMSLog.objects.filter(category=SMSLog.ALERT_YELLOW).count())
        self.assertEqual(0, SMSLog.objects.filter(category=SMSLog.ALERT_RED).count())
        
    
    def test_flood(self):
        
        today = datetime.today()
        
        # 40 to 100 in 2 hours
        
        indexs = range(0, 360)
        for i in indexs:
            Data.objects.create(sensor=self.s1, utrasonic=(i/6)+40, created=today-timedelta(minutes=360-i))
            
        self.assertEqual(0, SMSLog.objects.filter(category=SMSLog.ALERT_GREEN).count())
        self.assertEqual(5, SMSLog.objects.filter(category=SMSLog.ALERT_YELLOW).count())
        self.assertEqual(5, SMSLog.objects.filter(category=SMSLog.ALERT_RED).count())    
        
        yellow = SMSLog.objects.filter(category=SMSLog.ALERT_YELLOW).order_by('created')
        
        self.assertEqual(today-timedelta(minutes=120-5), yellow[0].created)
        self.assertEqual(today-timedelta(minutes=110-5), yellow[1].created)
        self.assertEqual(today-timedelta(minutes=100-5), yellow[2].created)
        self.assertEqual(today-timedelta(minutes=90-5),  yellow[3].created)
        self.assertEqual(today-timedelta(minutes=80-5),  yellow[4].created)
        
        red = SMSLog.objects.filter(category=SMSLog.ALERT_RED).order_by('created')
        
        self.assertEqual(today-timedelta(minutes=60-5), red[0].created)
        self.assertEqual(today-timedelta(minutes=50-5), red[1].created)
        self.assertEqual(today-timedelta(minutes=40-5), red[2].created)
        self.assertEqual(today-timedelta(minutes=30-5), red[3].created)
        self.assertEqual(today-timedelta(minutes=20-5), red[4].created)
                