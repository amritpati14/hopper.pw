# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'StatEntry'
        db.create_table(u'stats_statentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('stat_type', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('data', self.gf('jsonfield.fields.JSONField')(default={})),
        ))
        db.send_create_signal(u'stats', ['StatEntry'])


    def backwards(self, orm):
        # Deleting model 'StatEntry'
        db.delete_table(u'stats_statentry')


    models = {
        u'stats.statentry': {
            'Meta': {'object_name': 'StatEntry'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'stat_type': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['stats']