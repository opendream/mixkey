# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'DataDay.battery_median'
        db.add_column(u'domain_dataday', 'battery_median',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DataThirtyMinute.battery_median'
        db.add_column(u'domain_datathirtyminute', 'battery_median',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DataYear.battery_median'
        db.add_column(u'domain_datayear', 'battery_median',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DataTenMinute.battery_median'
        db.add_column(u'domain_datatenminute', 'battery_median',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Data.battery_median'
        db.add_column(u'domain_data', 'battery_median',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DataMonth.battery_median'
        db.add_column(u'domain_datamonth', 'battery_median',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DataWeek.battery_median'
        db.add_column(u'domain_dataweek', 'battery_median',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DataHour.battery_median'
        db.add_column(u'domain_datahour', 'battery_median',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'DataDay.battery_median'
        db.delete_column(u'domain_dataday', 'battery_median')

        # Deleting field 'DataThirtyMinute.battery_median'
        db.delete_column(u'domain_datathirtyminute', 'battery_median')

        # Deleting field 'DataYear.battery_median'
        db.delete_column(u'domain_datayear', 'battery_median')

        # Deleting field 'DataTenMinute.battery_median'
        db.delete_column(u'domain_datatenminute', 'battery_median')

        # Deleting field 'Data.battery_median'
        db.delete_column(u'domain_data', 'battery_median')

        # Deleting field 'DataMonth.battery_median'
        db.delete_column(u'domain_datamonth', 'battery_median')

        # Deleting field 'DataWeek.battery_median'
        db.delete_column(u'domain_dataweek', 'battery_median')

        # Deleting field 'DataHour.battery_median'
        db.delete_column(u'domain_datahour', 'battery_median')


    models = {
        u'domain.data': {
            'Meta': {'object_name': 'Data'},
            'battery': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'battery_median': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'humidity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raingauge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domain.Sensor']"}),
            'temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'utrasonic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'water_level': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'water_level_raw': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'domain.dataday': {
            'Meta': {'object_name': 'DataDay'},
            'battery': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'battery_median': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'humidity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raingauge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domain.Sensor']"}),
            'temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'utrasonic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'water_level': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'water_level_raw': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'domain.datahour': {
            'Meta': {'object_name': 'DataHour'},
            'battery': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'battery_median': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'humidity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raingauge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domain.Sensor']"}),
            'temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'utrasonic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'water_level': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'water_level_raw': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'domain.datamonth': {
            'Meta': {'object_name': 'DataMonth'},
            'battery': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'battery_median': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'humidity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raingauge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domain.Sensor']"}),
            'temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'utrasonic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'water_level': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'water_level_raw': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'domain.datatenminute': {
            'Meta': {'object_name': 'DataTenMinute'},
            'battery': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'battery_median': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'humidity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raingauge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domain.Sensor']"}),
            'temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'utrasonic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'water_level': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'water_level_raw': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'domain.datathirtyminute': {
            'Meta': {'object_name': 'DataThirtyMinute'},
            'battery': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'battery_median': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'humidity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raingauge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domain.Sensor']"}),
            'temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'utrasonic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'water_level': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'water_level_raw': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'domain.dataweek': {
            'Meta': {'object_name': 'DataWeek'},
            'battery': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'battery_median': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'humidity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raingauge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domain.Sensor']"}),
            'temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'utrasonic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'water_level': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'water_level_raw': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'domain.datayear': {
            'Meta': {'object_name': 'DataYear'},
            'battery': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'battery_median': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'humidity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raingauge': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['domain.Sensor']"}),
            'temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'utrasonic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'water_level': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'water_level_raw': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
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