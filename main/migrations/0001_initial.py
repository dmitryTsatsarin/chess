# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Member'
        db.create_table('main_member', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('elo', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('main', ['Member'])

        # Adding model 'Tournament'
        db.create_table('main_tournament', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tour_closed', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('main', ['Tournament'])

        # Adding model 'Tour'
        db.create_table('main_tour', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tour', self.gf('django.db.models.fields.IntegerField')()),
            ('player1', self.gf('django.db.models.fields.related.OneToOneField')(related_name='player1', unique=True, to=orm['main.Member'])),
            ('player2', self.gf('django.db.models.fields.related.OneToOneField')(related_name='player2', unique=True, null=True, to=orm['main.Member'])),
            ('points', self.gf('django.db.models.fields.FloatField')(null=True)),
        ))
        db.send_create_signal('main', ['Tour'])


    def backwards(self, orm):
        # Deleting model 'Member'
        db.delete_table('main_member')

        # Deleting model 'Tournament'
        db.delete_table('main_tournament')

        # Deleting model 'Tour'
        db.delete_table('main_tour')


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
            'player1': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'player1'", 'unique': 'True', 'to': "orm['main.Member']"}),
            'player2': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'player2'", 'unique': 'True', 'null': 'True', 'to': "orm['main.Member']"}),
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