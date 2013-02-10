# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Tour', fields ['player1']
        db.delete_unique('main_tour', ['player1_id'])

        # Removing unique constraint on 'Tour', fields ['player2']
        db.delete_unique('main_tour', ['player2_id'])


        # Changing field 'Tour.player2'
        db.alter_column('main_tour', 'player2_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['main.Member']))

        # Changing field 'Tour.player1'
        db.alter_column('main_tour', 'player1_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Member']))

    def backwards(self, orm):

        # Changing field 'Tour.player2'
        db.alter_column('main_tour', 'player2_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, null=True, to=orm['main.Member']))
        # Adding unique constraint on 'Tour', fields ['player2']
        db.create_unique('main_tour', ['player2_id'])


        # Changing field 'Tour.player1'
        db.alter_column('main_tour', 'player1_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['main.Member']))
        # Adding unique constraint on 'Tour', fields ['player1']
        db.create_unique('main_tour', ['player1_id'])


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
            'tour_closed': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['main']