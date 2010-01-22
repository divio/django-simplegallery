
from south.db import db
from django.db import models
from simplegallery.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'GalleryPublication'
        db.create_table('cmsplugin_gallerypublication', (
            ('cmsplugin_ptr', orm['simplegallery.GalleryPublication:cmsplugin_ptr']),
            ('gallery', orm['simplegallery.GalleryPublication:gallery']),
            ('aspect_ratio', orm['simplegallery.GalleryPublication:aspect_ratio']),
        ))
        db.send_create_signal('simplegallery', ['GalleryPublication'])
        
        # Adding model 'GalleryTranslation'
        db.create_table('simplegallery_gallery_translation', (
            ('id', orm['simplegallery.GalleryTranslation:id']),
            ('title', orm['simplegallery.GalleryTranslation:title']),
            ('description', orm['simplegallery.GalleryTranslation:description']),
            ('language_id', orm['simplegallery.GalleryTranslation:language_id']),
            ('master', orm['simplegallery.GalleryTranslation:master']),
        ))
        db.send_create_signal('simplegallery', ['GalleryTranslation'])
        
        # Adding model 'Image'
        db.create_table('simplegallery_image', (
            ('id', orm['simplegallery.Image:id']),
            ('gallery', orm['simplegallery.Image:gallery']),
            ('image', orm['simplegallery.Image:image']),
            ('page_link', orm['simplegallery.Image:page_link']),
            ('ordering', orm['simplegallery.Image:ordering']),
        ))
        db.send_create_signal('simplegallery', ['Image'])
        
        # Adding model 'CarouselImage'
        db.create_table('simplegallery_carouselimage', (
            ('id', orm['simplegallery.CarouselImage:id']),
            ('carousel_feature', orm['simplegallery.CarouselImage:carousel_feature']),
            ('image', orm['simplegallery.CarouselImage:image']),
            ('date', orm['simplegallery.CarouselImage:date']),
            ('title', orm['simplegallery.CarouselImage:title']),
            ('description', orm['simplegallery.CarouselImage:description']),
            ('title_2', orm['simplegallery.CarouselImage:title_2']),
            ('description_2', orm['simplegallery.CarouselImage:description_2']),
            ('page_link', orm['simplegallery.CarouselImage:page_link']),
            ('url', orm['simplegallery.CarouselImage:url']),
            ('ordering', orm['simplegallery.CarouselImage:ordering']),
        ))
        db.send_create_signal('simplegallery', ['CarouselImage'])
        
        # Adding model 'Gallery'
        db.create_table('simplegallery_gallery', (
            ('id', orm['simplegallery.Gallery:id']),
        ))
        db.send_create_signal('simplegallery', ['Gallery'])
        
        # Adding model 'CarouselFeature'
        db.create_table('cmsplugin_carouselfeature', (
            ('cmsplugin_ptr', orm['simplegallery.CarouselFeature:cmsplugin_ptr']),
            ('title', orm['simplegallery.CarouselFeature:title']),
            ('interval', orm['simplegallery.CarouselFeature:interval']),
            ('aspect_ratio', orm['simplegallery.CarouselFeature:aspect_ratio']),
        ))
        db.send_create_signal('simplegallery', ['CarouselFeature'])
        
        # Adding model 'ImageTranslation'
        db.create_table('simplegallery_image_translation', (
            ('id', orm['simplegallery.ImageTranslation:id']),
            ('title', orm['simplegallery.ImageTranslation:title']),
            ('description', orm['simplegallery.ImageTranslation:description']),
            ('language_id', orm['simplegallery.ImageTranslation:language_id']),
            ('master', orm['simplegallery.ImageTranslation:master']),
        ))
        db.send_create_signal('simplegallery', ['ImageTranslation'])
        
        # Creating unique_together for [language_id, master] on GalleryTranslation.
        db.create_unique('simplegallery_gallery_translation', ['language_id', 'master_id'])
        
        # Creating unique_together for [language_id, master] on ImageTranslation.
        db.create_unique('simplegallery_image_translation', ['language_id', 'master_id'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [language_id, master] on ImageTranslation.
        db.delete_unique('simplegallery_image_translation', ['language_id', 'master_id'])
        
        # Deleting unique_together for [language_id, master] on GalleryTranslation.
        db.delete_unique('simplegallery_gallery_translation', ['language_id', 'master_id'])
        
        # Deleting model 'GalleryPublication'
        db.delete_table('cmsplugin_gallerypublication')
        
        # Deleting model 'GalleryTranslation'
        db.delete_table('simplegallery_gallery_translation')
        
        # Deleting model 'Image'
        db.delete_table('simplegallery_image')
        
        # Deleting model 'CarouselImage'
        db.delete_table('simplegallery_carouselimage')
        
        # Deleting model 'Gallery'
        db.delete_table('simplegallery_gallery')
        
        # Deleting model 'CarouselFeature'
        db.delete_table('cmsplugin_carouselfeature')
        
        # Deleting model 'ImageTranslation'
        db.delete_table('simplegallery_image_translation')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'cms.cmsplugin': {
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Page']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'publisher_is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True', 'blank': 'True'}),
            'publisher_public': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'publisher_draft'", 'unique': 'True', 'null': 'True', 'to': "orm['cms.CMSPlugin']"}),
            'publisher_state': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.page': {
            'changed_by': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'created_by': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_navigation': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'menu_login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'moderator_state': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'blank': 'True'}),
            'navigation_extenders': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['cms.Page']"}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'publication_end_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'publisher_is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True', 'blank': 'True'}),
            'publisher_public': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'publisher_draft'", 'unique': 'True', 'null': 'True', 'to': "orm['cms.Page']"}),
            'publisher_state': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'reverse_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'soft_root': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'filer.file': {
            '_file_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            '_file_type_plugin_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'file_field': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'all_files'", 'null': 'True', 'to': "orm['filer.Folder']"}),
            'has_all_mandatory_data': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'original_filename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owned_files'", 'null': 'True', 'to': "orm['auth.User']"}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'filer.folder': {
            'Meta': {'unique_together': "(('parent', 'name'),)"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owned_folders'", 'null': 'True', 'to': "orm['auth.User']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['filer.Folder']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'filer.image': {
            '_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            '_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'default_alt_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'default_caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'file_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['filer.File']", 'unique': 'True', 'primary_key': 'True'}),
            'must_always_publish_author_credit': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'must_always_publish_copyright': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'subject_location': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'simplegallery.carouselfeature': {
            'Meta': {'db_table': "'cmsplugin_carouselfeature'"},
            'aspect_ratio': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'interval': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '3'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        'simplegallery.carouselimage': {
            'carousel_feature': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['simplegallery.CarouselFeature']"}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['filer.Image']"}),
            'ordering': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'page_link': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Page']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'title_2': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'simplegallery.gallery': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'simplegallery.gallerypublication': {
            'Meta': {'db_table': "'cmsplugin_gallerypublication'"},
            'aspect_ratio': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'gallery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['simplegallery.Gallery']"})
        },
        'simplegallery.gallerytranslation': {
            'Meta': {'unique_together': "(('language_id', 'master'),)", 'db_table': "'simplegallery_gallery_translation'"},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'to': "orm['simplegallery.Gallery']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'simplegallery.image': {
            'gallery': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['simplegallery.Gallery']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['filer.Image']"}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'page_link': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Page']", 'null': 'True', 'blank': 'True'})
        },
        'simplegallery.imagetranslation': {
            'Meta': {'unique_together': "(('language_id', 'master'),)", 'db_table': "'simplegallery_image_translation'"},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'to': "orm['simplegallery.Image']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'sites.site': {
            'Meta': {'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }
    
    complete_apps = ['simplegallery']
