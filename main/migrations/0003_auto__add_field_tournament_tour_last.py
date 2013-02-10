# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Tournament.tour_last'
        db.add_column('main_tournament', 'tour_last',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Tournament.tour_last'
        db.delete_column('main_tournament', 'tour_last')


    models = {
        'main.member': {
            'Meta': {'object_name': 'Member'},
            'elo': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.tour': {
            'Meta': {'object_name': 'Tour'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player1'", 'to': "orm['main.Member']"}),
            'player2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'player2'", 'null': 'True', 'to': "orm['main.Member']"}),
            'points': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'tour': ('django.db.models.fields.IntegerField', [], {})
        },
        'main.tournament': {
            'Meta': {'object_name': 'Tournament'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tour_closed': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'tour_last': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['main']