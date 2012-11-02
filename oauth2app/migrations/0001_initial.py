# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Client'
        db.create_table('oauth2app_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_index=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('submitted_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='client_submitted_by', null=True, to=orm['auth.User'])),
            ('approved_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='client_approved_by', null=True, to=orm['auth.User'])),
            ('removed_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='client_removed_by', null=True, to=orm['auth.User'])),
            ('submitted_time', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('approved_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('removed_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('submission_message', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('removal_message', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('auto_approve', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('counts_towards_contributions', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('action_taken', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('action_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='client_action_by', null=True, to=orm['auth.User'])),
            ('action_time', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('action_message', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('is_head', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('points_to_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True, null=True, blank=True)),
            ('primary_merge_from_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True, null=True, blank=True)),
            ('secondary_merge_from_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True, null=True, blank=True)),
            ('merge_event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trackable_object.MergeEvent'], null=True, blank=True)),
            ('cache_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('real_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='client_real_type', null=True, to=orm['contenttypes.ContentType'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=256, blank=True)),
            ('key', self.gf('django.db.models.fields.CharField')(default='597b76c283590c42c00c59aa67a5b7', max_length=30, db_index=True)),
            ('secret', self.gf('django.db.models.fields.CharField')(default='943a045473d860d4f3aa9f6d48b565', max_length=30)),
            ('redirect_uri', self.gf('oauth2app.models.CustomURLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('oauth2app', ['Client'])

        # Adding model 'AccessRange'
        db.create_table('oauth2app_accessrange', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('oauth2app', ['AccessRange'])

        # Adding model 'AccessToken'
        db.create_table('oauth2app_accesstoken', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oauth2app.Client'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('token', self.gf('django.db.models.fields.CharField')(default='8014e71be2', unique=True, max_length=10, db_index=True)),
            ('refresh_token', self.gf('django.db.models.fields.CharField')(null=True, default='b57d49430c', max_length=10, blank=True, unique=True, db_index=True)),
            ('mac_key', self.gf('django.db.models.fields.CharField')(default=None, max_length=20, unique=True, null=True, blank=True)),
            ('issue', self.gf('django.db.models.fields.PositiveIntegerField')(default=1351897074)),
            ('expire', self.gf('django.db.models.fields.PositiveIntegerField')(default=1352501874)),
            ('refreshable', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('oauth2app', ['AccessToken'])

        # Adding M2M table for field scope on 'AccessToken'
        db.create_table('oauth2app_accesstoken_scope', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('accesstoken', models.ForeignKey(orm['oauth2app.accesstoken'], null=False)),
            ('accessrange', models.ForeignKey(orm['oauth2app.accessrange'], null=False))
        ))
        db.create_unique('oauth2app_accesstoken_scope', ['accesstoken_id', 'accessrange_id'])

        # Adding model 'Code'
        db.create_table('oauth2app_code', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oauth2app.Client'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('key', self.gf('django.db.models.fields.CharField')(default='7a8026e92e098bab01e5211b92b34a', unique=True, max_length=30, db_index=True)),
            ('issue', self.gf('django.db.models.fields.PositiveIntegerField')(default=1351897074)),
            ('expire', self.gf('django.db.models.fields.PositiveIntegerField')(default=1351897194)),
            ('redirect_uri', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('oauth2app', ['Code'])

        # Adding M2M table for field scope on 'Code'
        db.create_table('oauth2app_code_scope', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('code', models.ForeignKey(orm['oauth2app.code'], null=False)),
            ('accessrange', models.ForeignKey(orm['oauth2app.accessrange'], null=False))
        ))
        db.create_unique('oauth2app_code_scope', ['code_id', 'accessrange_id'])

        # Adding model 'MACNonce'
        db.create_table('oauth2app_macnonce', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('access_token', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oauth2app.AccessToken'])),
            ('nonce', self.gf('django.db.models.fields.CharField')(max_length=30, db_index=True)),
        ))
        db.send_create_signal('oauth2app', ['MACNonce'])


    def backwards(self, orm):
        # Deleting model 'Client'
        db.delete_table('oauth2app_client')

        # Deleting model 'AccessRange'
        db.delete_table('oauth2app_accessrange')

        # Deleting model 'AccessToken'
        db.delete_table('oauth2app_accesstoken')

        # Removing M2M table for field scope on 'AccessToken'
        db.delete_table('oauth2app_accesstoken_scope')

        # Deleting model 'Code'
        db.delete_table('oauth2app_code')

        # Removing M2M table for field scope on 'Code'
        db.delete_table('oauth2app_code_scope')

        # Deleting model 'MACNonce'
        db.delete_table('oauth2app_macnonce')


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'oauth2app.accessrange': {
            'Meta': {'object_name': 'AccessRange'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'oauth2app.accesstoken': {
            'Meta': {'object_name': 'AccessToken'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oauth2app.Client']"}),
            'expire': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1352501874'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1351897074'}),
            'mac_key': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'refresh_token': ('django.db.models.fields.CharField', [], {'null': 'True', 'default': "'90069a68cb'", 'max_length': '10', 'blank': 'True', 'unique': 'True', 'db_index': 'True'}),
            'refreshable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'scope': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['oauth2app.AccessRange']", 'symmetrical': 'False'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'b2d6563cc8'", 'unique': 'True', 'max_length': '10', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'oauth2app.client': {
            'Meta': {'object_name': 'Client'},
            'action_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'client_action_by'", 'null': 'True', 'to': "orm['auth.User']"}),
            'action_message': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'action_taken': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'action_time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'client_approved_by'", 'null': 'True', 'to': "orm['auth.User']"}),
            'approved_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'auto_approve': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cache_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'counts_towards_contributions': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_index': 'True'}),
            'is_head': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'142e948dc037708d27ed48e7cec3c4'", 'max_length': '30', 'db_index': 'True'}),
            'merge_event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['trackable_object.MergeEvent']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'points_to_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'primary_merge_from_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'real_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'client_real_type'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'redirect_uri': ('oauth2app.models.CustomURLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'removal_message': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'removed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'client_removed_by'", 'null': 'True', 'to': "orm['auth.User']"}),
            'removed_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'secondary_merge_from_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'default': "'4b3772cd1a84437e681f051d7b7d69'", 'max_length': '30'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'submission_message': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'submitted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'client_submitted_by'", 'null': 'True', 'to': "orm['auth.User']"}),
            'submitted_time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '256', 'blank': 'True'})
        },
        'oauth2app.code': {
            'Meta': {'object_name': 'Code'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oauth2app.Client']"}),
            'expire': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1351897194'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1351897074'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'a44cd324b8f1f125c0faf31a741c75'", 'unique': 'True', 'max_length': '30', 'db_index': 'True'}),
            'redirect_uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'scope': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['oauth2app.AccessRange']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'oauth2app.macnonce': {
            'Meta': {'object_name': 'MACNonce'},
            'access_token': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oauth2app.AccessToken']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nonce': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'})
        },
        'trackable_object.mergeevent': {
            'Meta': {'object_name': 'MergeEvent'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['oauth2app']