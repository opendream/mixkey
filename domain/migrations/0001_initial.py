# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Project'
        db.create_table(u'domain_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('timezone', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('tel_key', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('tel_list', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('data_dict', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'domain', ['Project'])

        # Adding model 'Sensor'
        db.create_table(u'domain_sensor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domain.Project'])),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('formula', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lng', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('level_red', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('level_yellow', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('data_dict', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('tel_key', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('tel_list', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'domain', ['Sensor'])

        # Adding model 'SMSLog'
        db.create_table(u'domain_smslog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domain.Project'])),
            ('sensor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domain.Sensor'], null=True)),
            ('category', self.gf('django.db.models.fields.IntegerField')(default=4)),
            ('is_send', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('from_tel', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('to_tel', self.gf('django.db.models.fields.TextField')()),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('message_sid', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'domain', ['SMSLog'])

        # Adding model 'Data'
        db.create_table(u'domain_data', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sensor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domain.Sensor'])),
            ('utrasonic', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('temperature', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('humidity', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('raingauge', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('battery', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'domain', ['Data'])

        # Adding model 'DataTenMinute'
        db.create_table(u'domain_datatenminute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sensor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domain.Sensor'])),
            ('utrasonic', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('temperature', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('humidity', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('raingauge', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('battery', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'domain', ['DataTenMinute'])

        # Adding model 'DataThirtyMinute'
        db.create_table(u'domain_datathirtyminute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sensor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domain.Sensor'])),
            ('utrasonic', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('temperature', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('humidity', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('raingauge', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('battery', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'domain', ['DataThirtyMinute'])

        # Adding model 'DataHour'
        db.create_table(u'domain_datahour', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sensor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domain.Sensor'])),
            ('utrasonic', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('temperature', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('humidity', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('raingauge', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('battery', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'domain', ['DataHour'])

        # Adding model 'DataDay'
        db.create_table(u'domain_dataday', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sensor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domain.Sensor'])),
            ('utrasonic', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('temperature', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('humidity', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('raingauge', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('battery', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'domain', ['DataDay'])

        # Adding model 'DataWeek'
        db.create_table(u'domain_dataweek', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sensor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domain.Sensor'])),
            ('utrasonic', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('temperature', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('humidity', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('raingauge', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('battery', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'domain', ['DataWeek'])

        # Adding model 'DataMonth'
        db.create_table(u'domain_datamonth', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sensor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domain.Sensor'])),
            ('utrasonic', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('temperature', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('humidity', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('raingauge', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('battery', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'domain', ['DataMonth'])

        # Adding model 'DataYear'
        db.create_table(u'domain_datayear', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sensor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['domain.Sensor'])),
            ('utrasonic', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('temperature', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('humidity', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('raingauge', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('battery', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'domain', ['DataYear'])


    def backwards(self, orm):
        # Deleting model 'Project'
        db.delete_table(u'domain_project')

        # Deleting model 'Sensor'
        db.delete_table(u'domain_sensor')

        # Deleting model 'SMSLog'
        db.delete_table(u'domain_smslog')

        # Deleting model 'Data'
        db.delete_table(u'domain_data')

        # Deleting model 'DataTenMinute'
        db.delete_table(u'domain_datatenminute')

        # Deleting model 'DataThirtyMinute'
        db.delete_table(u'domain_datathirtyminute')

        # Deleting model 'DataHour'
        db.delete_table(u'domain_datahour')

        # Deleting model 'DataDay'
        db.delete_table(u'domain_dataday')

        # Deleting model 'DataWeek'
        db.delete_table(u'domain_dataweek')

        # Deleting model 'DataMonth'
        db.delete_table(u'domain_datamonth')

        # Deleting model 'DataYear'
        db.delete_table(u'domain_datayear')


    models = {
        u'domain.data': {
            'Meta': {'object_name': 'Data'},
            'battery': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'humidity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raingauge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domain.Sensor']"}),
            'temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'utrasonic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'domain.dataday': {
            'Meta': {'object_name': 'DataDay'},
            'battery': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'humidity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raingauge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domain.Sensor']"}),
            'temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'utrasonic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'domain.datahour': {
            'Meta': {'object_name': 'DataHour'},
            'battery': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'humidity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raingauge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domain.Sensor']"}),
            'temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'utrasonic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'domain.datamonth': {
            'Meta': {'object_name': 'DataMonth'},
            'battery': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'humidity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raingauge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domain.Sensor']"}),
            'temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'utrasonic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'domain.datatenminute': {
            'Meta': {'object_name': 'DataTenMinute'},
            'battery': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'humidity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raingauge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domain.Sensor']"}),
            'temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'utrasonic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'domain.datathirtyminute': {
            'Meta': {'object_name': 'DataThirtyMinute'},
            'battery': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'humidity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raingauge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domain.Sensor']"}),
            'temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'utrasonic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'domain.dataweek': {
            'Meta': {'object_name': 'DataWeek'},
            'battery': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'humidity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raingauge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domain.Sensor']"}),
            'temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'utrasonic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'domain.datayear': {
            'Meta': {'object_name': 'DataYear'},
            'battery': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'humidity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raingauge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domain.Sensor']"}),
            'temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'utrasonic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'domain.project': {
            'Meta': {'object_name': 'Project'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data_dict': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tel_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tel_list': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'domain.sensor': {
            'Meta': {'object_name': 'Sensor'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data_dict': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'formula': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'level_red': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'level_yellow': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lng': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domain.Project']"}),
            'tel_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tel_list': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'domain.smslog': {
            'Meta': {'object_name': 'SMSLog'},
            'category': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'from_tel': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_send': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'message_sid': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domain.Project']"}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domain.Sensor']", 'null': 'True'}),
            'to_tel': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['domain']