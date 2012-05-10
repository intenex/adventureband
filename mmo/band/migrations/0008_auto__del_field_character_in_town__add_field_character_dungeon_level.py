# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Character.in_town'
        db.delete_column('band_character', 'in_town')

        # Adding field 'Character.dungeon_level'
        db.add_column('band_character', 'dungeon_level', self.gf('django.db.models.fields.IntegerField')(default=101), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Character.in_town'
        db.add_column('band_character', 'in_town', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True), keep_default=False)

        # Deleting field 'Character.dungeon_level'
        db.delete_column('band_character', 'dungeon_level')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'band.character': {
            'Meta': {'object_name': 'Character'},
            'body': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True'}),
            'char_class': ('django.db.models.fields.CharField', [], {'default': "'W'", 'max_length': '1'}),
            'charisma': ('django.db.models.fields.IntegerField', [], {}),
            'constitution': ('django.db.models.fields.IntegerField', [], {}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {}),
            'current_hp': ('django.db.models.fields.IntegerField', [], {}),
            'dexterity': ('django.db.models.fields.IntegerField', [], {}),
            'dungeon_level': ('django.db.models.fields.IntegerField', [], {}),
            'exp': ('django.db.models.fields.IntegerField', [], {}),
            'feet': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True'}),
            'first_time': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gold': ('django.db.models.fields.IntegerField', [], {}),
            'hands': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True'}),
            'head': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intelligence': ('django.db.models.fields.IntegerField', [], {}),
            'left_finger': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'max_hp': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name_lower': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'quiver': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True'}),
            'race': ('django.db.models.fields.CharField', [], {'default': "'E'", 'max_length': '1'}),
            'ranged': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True'}),
            'right_finger': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'default': "'M'", 'max_length': '1'}),
            'shield': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True'}),
            'strength': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'weapon': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True'}),
            'wisdom': ('django.db.models.fields.IntegerField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['band']
